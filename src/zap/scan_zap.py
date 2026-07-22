#!/usr/bin/env python3
"""Trình chạy OWASP ZAP tự động cho lab EShop local.

Script này điều phối toàn bộ vòng đời scan: khởi động hoặc kết nối ZAP,
chuẩn bị context/auth của EShop, chọn scan policy, chạy spider/active scan,
và ghi report ra file do người dùng chọn.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from collections.abc import Iterable, Mapping
from pathlib import Path
from urllib.parse import urlparse

from zapv2 import ZAPv2

from zap_runtime import (
    CONTEXT_NAME,
    cleanup_authenticated_context,
    configure_authenticated_context,
    ensure_context,
    get_credential,
    load_dotenv,
    login_for_token,
    validate_target,
    verify_authenticated_session,
)

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_REPORT_PATH = SCRIPT_DIR / "output" / "zap_scan_report.html"
LOCAL_ZAP_HOSTS = {"localhost", "127.0.0.1"}
OFFICIAL_REPORT_TEMPLATES = {
    "html": "modern",
    "json": "traditional-json-plus",
}
SCAN_MODE_BASIC = "basic"
SCAN_MODE_OWASP_TOP10_2025 = "owasp-top10-2025"
OWASP_2025_TAG_PREFIX = "OWASP_2025_"
OWASP_2025_SCAN_POLICY_NAME = "owasp-top10-2025"
OWASP_2025_ACTIVE_SCANNER_IDS = {
    "0",
    "6",
    "7",
    "41",
    "42",
    "43",
    "10045",
    "10047",
    "10048",
    "10051",
    "10058",
    "10095",
    "10106",
    "10107",
    "10205",
    "20012",
    "20014",
    "20015",
    "20016",
    "20017",
    "20018",
    "20019",
    "30001",
    "30002",
    "30003",
    "40003",
    "40008",
    "40009",
    "40012",
    "40013",
    "40014",
    "40015",
    "40016",
    "40017",
    "40018",
    "40019",
    "40020",
    "40021",
    "40022",
    "40023",
    "40024",
    "40025",
    "40026",
    "40027",
    "40028",
    "40029",
    "40031",
    "40032",
    "40033",
    "40034",
    "40035",
    "40038",
    "40039",
    "40040",
    "40042",
    "40043",
    "40044",
    "40045",
    "40046",
    "40047",
    "40048",
    "90017",
    "90018",
    "90019",
    "90020",
    "90021",
    "90023",
    "90024",
    "90025",
    "90026",
    "90027",
    "90028",
    "90029",
    "90034",
    "90035",
    "90036",
    "90037",
    "90039",
    "100043",
    "100044",
}


def _env_bool(name: str, default: bool = False) -> bool:
    """Đọc các giá trị boolean phổ biến từ biến môi trường cho default CLI."""
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _positive_int(value: str) -> int:
    """Parse số nguyên dương cho các giới hạn scan từ CLI/env."""
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a positive integer") from exc
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return parsed


def _env_positive_int(name: str) -> int | None:
    """Đọc số nguyên dương từ biến môi trường; bỏ qua khi chưa cấu hình."""
    value = os.getenv(name)
    if value is None or value.strip() == "":
        return None
    return _positive_int(value)


def build_parser(load_env: bool = True) -> argparse.ArgumentParser:
    """Tạo CLI parser; test có thể bỏ qua việc load file .env local."""
    if load_env:
        load_dotenv()
    parser = argparse.ArgumentParser(description="Run an automated OWASP ZAP scan for local EShop")
    parser.add_argument("--target", default=os.getenv("ZAP_TARGET", "http://localhost:3000"))
    parser.add_argument("--zap-url", default=os.getenv("ZAP_URL", "http://localhost:8090"))
    parser.add_argument("--api-key", default=os.getenv("ZAP_API_KEY", ""))
    parser.add_argument(
        "--auth-role",
        choices=["none", "user", "admin"],
        default=os.getenv("ZAP_AUTH_ROLE", "none"),
    )
    parser.add_argument(
        "--forced-user",
        action=argparse.BooleanOptionalAction,
        default=_env_bool("ZAP_FORCED_USER"),
    )
    parser.add_argument(
        "--ajax-spider",
        action=argparse.BooleanOptionalAction,
        default=_env_bool("ZAP_AJAX_SPIDER"),
    )
    parser.add_argument(
        "--max-urls",
        type=_positive_int,
        default=_env_positive_int("ZAP_MAX_URLS"),
        help=(
            "Giới hạn số URL được phép active scan. Nếu crawl vượt giới hạn, "
            "script bỏ qua active scan để tránh quá tải RAM."
        ),
    )
    parser.add_argument(
        "--scan-mode",
        default=os.getenv("ZAP_SCAN_MODE", SCAN_MODE_BASIC),
        choices=[SCAN_MODE_BASIC, SCAN_MODE_OWASP_TOP10_2025],
        help=(
            "Chọn policy active scan: basic dùng rule mặc định của ZAP, "
            "owasp-top10-2025 chỉ bật các scanner có tag OWASP_2025_*."
        ),
    )

    parser.add_argument(
        "--report-format",
        default=os.getenv("ZAP_REPORT_FORMAT", "html"),
        choices=["html", "json"],
        help="Kiểu file report phục vụ pipeline: html để đọc thủ công, json để AI/tool xử lý.",
    )
    parser.add_argument(
        "--report-file",
        "--output-file",
        dest="report_file",
        default=os.getenv("ZAP_REPORT_FILE", str(DEFAULT_REPORT_PATH)),
        help=f"Report output path/name. Default: {DEFAULT_REPORT_PATH}",
    )
    return parser


def validate_authenticated_zap_url(zap_url: str) -> str:
    """Chặn authenticated scan qua ZAP proxy remote hoặc URL sai định dạng."""
    parsed = urlparse(zap_url)
    try:
        parsed.port
    except ValueError as exc:
        raise ValueError(
            "Authenticated scans require --zap-url to be a local HTTP ZAP daemon URL"
        ) from exc
    if parsed.scheme != "http" or parsed.hostname not in LOCAL_ZAP_HOSTS:
        raise ValueError(
            "Authenticated scans require --zap-url to be a local HTTP ZAP daemon URL"
        )
    return zap_url


def wait_for_zap(zap, timeout: int = 60) -> str:
    """Chờ đến khi ZAP daemon sẵn sàng và trả về version qua API."""
    deadline = time.monotonic() + timeout
    last_error = None
    while time.monotonic() < deadline:
        try:
            return zap.core.version
        except Exception as exc:
            last_error = exc
            time.sleep(1)
    raise RuntimeError(f"ZAP daemon was not ready within {timeout}s: {last_error}")


def check_scan_status(
    zap,
    scan_id: str | None,
    scan_type: str = "Spider",
    timeout: int = 1800,
    poll_interval: int = 5,
) -> None:
    """Theo dõi tiến độ một scan của ZAP cho đến khi xong hoặc timeout."""
    print(f"[*] Starting {scan_type} (Scan ID: {scan_id})...")
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if scan_type == "Spider":
            status = int(zap.spider.status(scan_id))
        elif scan_type == "Active Scan":
            status = int(zap.ascan.status(scan_id))
        elif scan_type == "AJAX Spider":
            status = str(zap.ajaxSpider.status)
            if status.lower() == "stopped":
                print(f"\n[+] {scan_type} completed.")
                return
            print(f"\r[*] {scan_type} progress: running...", end="")
            time.sleep(poll_interval)
            continue
        else:
            raise ValueError(f"Unsupported scan type: {scan_type}")

        print(f"\r[*] {scan_type} progress: {status}%", end="")
        if status >= 100:
            print(f"\n[+] {scan_type} completed.")
            return
        time.sleep(poll_interval)
    raise RuntimeError(f"{scan_type} did not complete within {timeout}s")


def wait_for_passive_scan(zap, timeout: int = 600, poll_interval: int = 2) -> None:
    """Chờ passive scanner xử lý hết các message ZAP đã thấy."""
    print("\n--- [3/4] PASSIVE SCAN ---")
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        records_to_scan = int(zap.pscan.records_to_scan)
        if records_to_scan <= 0:
            print("\n[+] Passive scan completed.")
            return
        print(f"\r[*] Waiting for Passive Scan to process {records_to_scan} records...", end="")
        time.sleep(poll_interval)
    raise RuntimeError(f"Passive scan did not complete within {timeout}s")


def _scanner_records(scanners: object) -> list[Mapping[str, object]]:
    """Chuẩn hóa payload scanner từ ZAP về danh sách mapping."""
    if isinstance(scanners, Mapping):
        for key in ("scanners", "scanner", "rules", "data"):
            value = scanners.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, Mapping)]
        return [scanners]
    if isinstance(scanners, list):
        return [item for item in scanners if isinstance(item, Mapping)]
    if isinstance(scanners, tuple):
        return [item for item in scanners if isinstance(item, Mapping)]
    if isinstance(scanners, Iterable) and not isinstance(scanners, (str, bytes)):
        return [item for item in scanners if isinstance(item, Mapping)]
    return []


def _scanner_id(scanner: Mapping[str, object]) -> str | None:
    """Trích ID rule từ một record scanner."""
    for key in ("id", "scannerId", "scanRuleId", "ruleId"):
        value = scanner.get(key)
        if value is not None:
            return str(value)
    return None


def _base_scanner_id(scanner_id: str) -> str:
    """Chuẩn hóa ID biến thể như 40014-1 về scanner chính 40014."""
    return scanner_id.split("-", 1)[0]


def _flatten_tags(raw_tags: object) -> set[str]:
    """Chuyển các kiểu biểu diễn tag của ZAP thành tập chuỗi phẳng."""
    tags: set[str] = set()
    if raw_tags is None:
        return tags
    if isinstance(raw_tags, str):
        parts = raw_tags.replace(",", " ").replace(";", " ").split()
        tags.update(part.strip() for part in parts if part.strip())
        return tags
    if isinstance(raw_tags, Mapping):
        for key, value in raw_tags.items():
            if isinstance(key, str) and key.strip():
                tags.add(key.strip())
            if isinstance(value, str) and value.strip():
                tags.add(value.strip())
            elif isinstance(value, Mapping):
                tags.update(_flatten_tags(value))
            elif isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
                for item in value:
                    tags.update(_flatten_tags(item))
            elif value is not None:
                tags.add(str(value))
        return tags
    if isinstance(raw_tags, Iterable):
        for item in raw_tags:
            tags.update(_flatten_tags(item))
        return tags
    tags.add(str(raw_tags))
    return tags


def _scanner_tags(scanner: Mapping[str, object]) -> set[str]:
    """Lấy tập tag của scanner từ nhiều schema response khác nhau của ZAP."""
    for key in ("alertTags", "alerttags", "tags", "tag"):
        if key in scanner:
            return _flatten_tags(scanner.get(key))
    return set()


def _top10_2025_scanner_ids(zap) -> tuple[list[str], list[str]]:
    """Tìm scanner IDs có tag OWASP 2025 để dùng cho policy giới hạn."""
    scanners = _scanner_records(zap.ascan.scanners())
    selected_ids: list[str] = []
    all_ids: list[str] = []
    for scanner in scanners:
        scanner_id = _scanner_id(scanner)
        if scanner_id is None:
            continue
        scanner_id = _base_scanner_id(scanner_id)
        if scanner_id not in all_ids:
            all_ids.append(scanner_id)
        tags = _scanner_tags(scanner)
        if (
            any(tag.startswith(OWASP_2025_TAG_PREFIX) for tag in tags)
            and scanner_id not in selected_ids
        ):
            selected_ids.append(scanner_id)
    if selected_ids:
        return selected_ids, all_ids
    selected_ids = [
        scanner_id for scanner_id in all_ids if scanner_id in OWASP_2025_ACTIVE_SCANNER_IDS
    ]
    return selected_ids, all_ids


def configure_scan_policy(zap, scan_mode: str = SCAN_MODE_BASIC) -> str | None:
    """Cấu hình policy active scan theo mode người dùng chọn."""
    if scan_mode == SCAN_MODE_BASIC:
        print("[*] Scan mode: basic ZAP default enabled rules.")
        return None

    if scan_mode != SCAN_MODE_OWASP_TOP10_2025:
        raise ValueError(f"Unsupported scan mode: {scan_mode}")

    print("[*] Scan mode: OWASP Top 10 2025 tag-based policy.")
    try:
        zap.ascan.remove_scan_policy(OWASP_2025_SCAN_POLICY_NAME)
    except Exception:
        pass
    zap.ascan.add_scan_policy(OWASP_2025_SCAN_POLICY_NAME)
    selected_ids, all_ids = _top10_2025_scanner_ids(zap)
    if not selected_ids:
        raise RuntimeError(
            "No OWASP Top 10 2025 active scanners were available in this ZAP install."
        )
    if all_ids:
        zap.ascan.disable_scanners(",".join(all_ids), scanpolicyname=OWASP_2025_SCAN_POLICY_NAME)
    zap.ascan.enable_scanners(",".join(selected_ids), scanpolicyname=OWASP_2025_SCAN_POLICY_NAME)
    print(
        f"[*] Enabled {len(selected_ids)} OWASP Top 10 2025 active scanners "
        f"in policy {OWASP_2025_SCAN_POLICY_NAME}."
    )
    return OWASP_2025_SCAN_POLICY_NAME


def _same_origin(url: str, target: str) -> bool:
    """Kiểm tra URL có cùng scheme/host/port với target scan hay không."""
    parsed_url = urlparse(url)
    parsed_target = urlparse(target)
    return (
        parsed_url.scheme == parsed_target.scheme
        and parsed_url.hostname == parsed_target.hostname
        and parsed_url.port == parsed_target.port
    )


def discovered_target_urls(zap, target: str) -> list[str]:
    """Lấy danh sách URL cùng origin mà ZAP đã ghi nhận cho target."""
    try:
        urls = zap.core.urls(baseurl=target)
    except TypeError:
        urls = zap.core.urls()
    return sorted(
        {url for url in urls if isinstance(url, str) and _same_origin(url, target)}
    )


def execute_scan(
    zap,
    target: str,
    context_id: str,
    ajax_spider: bool,
    scan_policy_name: str | None = None,
    max_urls: int | None = None,
) -> None:
    """Chạy crawl, đợi passive scan, rồi active scan cho một target URL."""
    print(f"[*] Opening target URL: {target}")
    zap.urlopen(target)
    time.sleep(2)

    print("\n--- [1/4] TRADITIONAL SPIDER ---")
    scan_id = zap.spider.scan(target, contextname=CONTEXT_NAME)
    check_scan_status(zap, scan_id, scan_type="Spider")

    print("\n--- [2/4] AJAX SPIDER ---")
    if ajax_spider:
        zap.ajaxSpider.scan(target, inscope="true", contextname=CONTEXT_NAME)
        check_scan_status(zap, None, scan_type="AJAX Spider")
    else:
        print("[*] Skipping AJAX Spider. Use --ajax-spider for SPA targets.")

    wait_for_passive_scan(zap)

    if max_urls is not None:
        discovered_urls = discovered_target_urls(zap, target)
        discovered_count = len(discovered_urls)
        print(f"\n[*] URL budget: discovered {discovered_count}/{max_urls} URLs for active scan.")
        if discovered_count > max_urls:
            print(
                "[!] Skipping Active Scan because URL budget was exceeded. "
                "Reduce AJAX Spider scope/time or increase --max-urls if this is expected."
            )
            return

    print("\n--- [4/4] ACTIVE SCAN ---")
    ascan_id = zap.ascan.scan(target, contextid=context_id, scanpolicyname=scan_policy_name)
    check_scan_status(zap, ascan_id, scan_type="Active Scan")


def write_report(zap, report_format: str, report_file: Path) -> None:
    """Ghi report ZAP theo format đã chọn vào path tuyệt đối hoặc tương đối."""
    report_path = report_file
    if not report_path.is_absolute():
        report_path = (Path.cwd() / report_path).resolve()
    report_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"\n[*] Generating {report_format.upper()} report: {report_path}")
    template = OFFICIAL_REPORT_TEMPLATES.get(report_format)
    if template is None:
        raise ValueError(f"Unsupported report format: {report_format}")

    try:
        # Dùng official Report Generation add-on để report có các metadata mới như alert tags.
        zap.reports.generate(
            title="EShop ZAP Scan Report",
            template=template,
            reportfilename=report_path.name,
            reportdir=str(report_path.parent),
            display="false",
        )
        if report_path.exists():
            print(f"[+] Report written to: {report_path}")
            return
        print(f"[!] Official Report Generation did not create the file {report_path}; falling back to core report.")
    except Exception as exc:
        print(f"[!] Official Report Generation failed, falling back to core report: {exc}")

    if report_format == "html":
        report = zap.core.htmlreport()
    elif report_format == "json":
        report = zap.core.jsonreport()
    else:
        raise ValueError(f"Unsupported report format: {report_format}")

    report_path.write_text(report, encoding="utf-8")
    print(f"[+] Report written to: {report_path}")


def print_alert_summary(zap, target: str) -> None:
    """In tóm tắt số lượng alert theo risk level cho target."""
    print("\n[*] Summarizing ZAP alerts...")
    alerts = zap.core.alerts(baseurl=target)
    alert_summary: dict[str, int] = {}
    for alert in alerts:
        risk = alert.get("risk", "Informational")
        alert_summary[risk] = alert_summary.get(risk, 0) + 1

    print("\n" + "=" * 40)
    print("          ZAP SCAN SUMMARY          ")
    print("=" * 40)
    print(f"Target       : {target}")
    print(f"Total alerts : {len(alerts)}")
    for risk_level, count in alert_summary.items():
        print(f" - {risk_level:<12}: {count}")
    print("=" * 40)


def run(args) -> int:
    """Điều phối vòng đời scan và kết nối tới ZAP daemon bên ngoài."""
    zap = None
    auth_configured = False
    exit_code = 0
    try:
        target = validate_target(args.target)
        if args.auth_role != "none":
            validate_authenticated_zap_url(args.zap_url)
        report_path = Path(args.report_file)
        if not report_path.is_absolute():
            report_path = (Path.cwd() / report_path).resolve()
        zap = ZAPv2(apikey=args.api_key, proxies={"http": args.zap_url, "https": args.zap_url})
        version = wait_for_zap(zap)
        print(f"[+] Connected to ZAP {version} at {args.zap_url}")
        credential = get_credential(args.auth_role)
        context_id = ensure_context(zap)
        if credential:
            token = login_for_token(args.zap_url, credential)
            state = configure_authenticated_context(zap, credential, token, args.forced_user)
            auth_configured = True
            context_id = state.context_id
            verify_authenticated_session(args.zap_url)
        scan_policy_name = configure_scan_policy(zap, args.scan_mode)
        execute_scan(
            zap,
            target,
            context_id,
            args.ajax_spider,
            scan_policy_name,
            args.max_urls,
        )
        print_alert_summary(zap, target)
        write_report(zap, args.report_format, report_path)
    except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as exc:
        print(f"[!] {exc}", file=sys.stderr)
        exit_code = 1
    finally:
        if zap is not None and auth_configured:
            try:
                cleanup_authenticated_context(zap, args.forced_user)
            except Exception as exc:
                print(f"[!] Failed to clean up authenticated ZAP context: {exc}", file=sys.stderr)
                exit_code = 1
    return exit_code


def main() -> None:
    """Entrypoint khi chạy file này trực tiếp bằng Python."""
    raise SystemExit(run(build_parser().parse_args()))


if __name__ == "__main__":
    main()
