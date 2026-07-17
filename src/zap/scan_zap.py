#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

from zapv2 import ZAPv2

from zap_runtime import (
    CONTEXT_NAME,
    ZapDockerManager,
    cleanup_authenticated_context,
    configure_authenticated_context,
    ensure_context,
    get_credential,
    login_for_token,
    validate_target,
    verify_authenticated_session,
)

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_REPORT_PATH = SCRIPT_DIR / "output" / "zap_scan_report.html"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run an automated OWASP ZAP scan for local EShop")
    parser.add_argument("--target", default="http://localhost:3000")
    parser.add_argument("--zap-url", default="http://localhost:8090")
    parser.add_argument("--api-key", default="")
    parser.add_argument("--auth-role", choices=["none", "user", "admin"], default="none")
    parser.add_argument("--forced-user", action="store_true")
    parser.add_argument("--ajax-spider", action="store_true")
    parser.add_argument("--external-zap", action="store_true")
    parser.add_argument("--report-format", default="html", choices=["html", "json", "xml", "md"])
    parser.add_argument("--report-file", default=str(DEFAULT_REPORT_PATH))
    return parser


def wait_for_zap(zap, timeout: int = 60) -> str:
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


def execute_scan(zap, target: str, context_id: str, ajax_spider: bool) -> None:
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

    print("\n--- [4/4] ACTIVE SCAN ---")
    ascan_id = zap.ascan.scan(target, contextid=context_id)
    check_scan_status(zap, ascan_id, scan_type="Active Scan")


def write_report(zap, report_format: str, report_file: Path) -> None:
    report_path = report_file
    if not report_path.is_absolute():
        report_path = (Path.cwd() / report_path).resolve()
    report_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"\n[*] Generating {report_format.upper()} report: {report_path}")
    if report_format == "html":
        report = zap.core.htmlreport()
    elif report_format == "json":
        report = zap.core.jsonreport()
    elif report_format == "xml":
        report = zap.core.xmlreport()
    elif report_format == "md":
        report = zap.core.mdreport()
    else:
        raise ValueError(f"Unsupported report format: {report_format}")

    report_path.write_text(report, encoding="utf-8")
    print(f"[+] Report written to: {report_path}")


def print_alert_summary(zap, target: str) -> None:
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
    manager = None
    zap = None
    auth_configured = False
    exit_code = 0
    try:
        target = validate_target(args.target)
        if not args.external_zap:
            manager = ZapDockerManager(port=urlparse(args.zap_url).port or 8090)
        if manager:
            manager.start()
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
        execute_scan(zap, target, context_id, args.ajax_spider)
        print_alert_summary(zap, target)
        write_report(zap, args.report_format, Path(args.report_file))
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
        if manager is not None:
            try:
                manager.stop()
            except Exception as exc:
                print(f"[!] Failed to stop ZAP Docker manager: {exc}", file=sys.stderr)
                exit_code = 1
    return exit_code


def main() -> None:
    raise SystemExit(run(build_parser().parse_args()))


if __name__ == "__main__":
    main()
