#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI-assisted triage for OWASP ZAP reports.

Default usage:
    python docs/zap/ai_triage_zap.py

With Gemini:
    GEMINI_API_KEY=... python docs/zap/ai_triage_zap.py --use-ai
"""

from __future__ import annotations

import argparse
import dataclasses
import html
import json
import os
import re
import sys
import textwrap
import urllib.error
import urllib.request
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_INPUT_DIR = SCRIPT_DIR / "output"
DEFAULT_OUTPUT = SCRIPT_DIR / "ai_triage_output.md"
DEFAULT_SUBMISSION = Path("submission/Team_Work_Assignment.md")
DEFAULT_MODEL = "gemini-2.5-flash"
GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
RISK_ORDER = {"High": 0, "Medium": 1, "Low": 2, "Informational": 3, "Info": 3, "Unknown": 4}
SUBMISSION_START = "<!-- ZAP_AI_TRIAGE_START -->"
SUBMISSION_END = "<!-- ZAP_AI_TRIAGE_END -->"


@dataclasses.dataclass(frozen=True)
class Alert:
    name: str
    risk: str
    confidence: str = ""
    method: str = ""
    url: str = ""
    parameter: str = ""
    evidence: str = ""
    solution: str = ""
    description: str = ""
    site: str = ""


def strip_tags(value: str) -> str:
    text = re.sub(r"<br\s*/?>", "\n", value, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r"\n\s+", "\n", text)
    return text.strip()


def collapse_ws(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def extract_labeled_value(text: str, label: str) -> str:
    pattern = rf"{re.escape(label)}\s*:\s*(.+?)(?:\n|$)"
    match = re.search(pattern, text, flags=re.IGNORECASE)
    return collapse_ws(match.group(1)) if match else ""


def split_method_url(text: str) -> tuple[str, str]:
    match = re.search(r"\b(GET|POST|PUT|PATCH|DELETE|OPTIONS|HEAD)\s+(https?://[^\n]+)", text)
    if not match:
        return "", ""
    return match.group(1), html.unescape(match.group(2)).rstrip(".,")


def parse_table_rows(report_html: str) -> list[Alert]:
    alerts: list[Alert] = []
    for row in re.findall(r"<tr\b[^>]*>(.*?)</tr>", report_html, flags=re.IGNORECASE | re.DOTALL):
        cells = re.findall(r"<t[dh]\b[^>]*>(.*?)</t[dh]>", row, flags=re.IGNORECASE | re.DOTALL)
        if len(cells) < 3:
            continue
        text_cells = [strip_tags(cell) for cell in cells]
        joined = "\n".join(text_cells)
        risk = next((risk for risk in RISK_ORDER if re.search(rf"\b{risk}\b", joined, re.IGNORECASE)), "")
        method, url = split_method_url(joined)
        if not risk or not url:
            continue
        name = text_cells[0]
        if name.lower() in {"risk level", "alert", "name"} and len(text_cells) > 1:
            name = text_cells[1]
        alerts.append(
            Alert(
                name=collapse_ws(name),
                risk="Informational" if risk == "Info" else risk,
                confidence=next(
                    (level for level in ("User Confirmed", "High", "Medium", "Low") if re.search(rf"\b{level}\b", joined)),
                    "",
                ),
                method=method,
                url=url,
                parameter=extract_labeled_value(joined, "Parameter"),
                evidence=extract_labeled_value(joined, "Evidence"),
                solution=extract_labeled_value(joined, "Solution"),
                description=extract_labeled_value(joined, "Description"),
            )
        )
    return alerts


def parse_details_sections(report_html: str) -> list[Alert]:
    alerts: list[Alert] = []
    risk_blocks = re.findall(
        r"<li id=\"alerts--risk-[^>]+>(.*?)(?=<li id=\"alerts--risk-|<section id=\"appendix\"|</main>)",
        report_html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    for block in risk_blocks:
        risk_match = re.search(r'class="risk-level">([^<]+)</span>', block, flags=re.IGNORECASE)
        confidence_match = re.search(r'class="confidence-level">([^<]+)</span>', block, flags=re.IGNORECASE)
        risk = strip_tags(risk_match.group(1)) if risk_match else "Unknown"
        confidence = strip_tags(confidence_match.group(1)) if confidence_match else ""
        site_match = re.search(r'class="site">([^<]+)</span>', block, flags=re.IGNORECASE)
        site = strip_tags(site_match.group(1)) if site_match else ""

        detail_sections = re.findall(r"<details\b[^>]*>(.*?)</details>", block, flags=re.IGNORECASE | re.DOTALL)
        for section in detail_sections:
            summary_match = re.search(r"<summary[^>]*>(.*?)</summary>", section, flags=re.IGNORECASE | re.DOTALL)
            name_match = re.search(r"<h5>\s*<a[^>]*>(.*?)</a>", block[: block.find(section)], flags=re.IGNORECASE | re.DOTALL)
            if not summary_match or not name_match:
                continue
            summary = strip_tags(summary_match.group(1))
            method, url = split_method_url(summary)
            if not url:
                continue
            section_text = strip_tags(section)
            alerts.append(
                Alert(
                    name=strip_tags(name_match.group(1)),
                    risk=risk,
                    confidence=confidence,
                    method=method,
                    url=url,
                    parameter=extract_labeled_value(section_text, "Parameter"),
                    evidence=extract_labeled_value(section_text, "Evidence"),
                    solution=extract_labeled_value(section_text, "Solution"),
                    description=extract_labeled_value(section_text, "Alert description"),
                    site=site,
                )
            )
    return alerts


def parse_classic_results(report_html: str) -> list[Alert]:
    alerts: list[Alert] = []
    tables = re.findall(
        r"<table\b[^>]*class=\"results\"[^>]*>(.*?)</table>",
        report_html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    for table in tables:
        header_match = re.search(
            r"<th\b[^>]*class=\"risk-[^>]*>.*?<div>(.*?)</div>.*?</th>\s*<th\b[^>]*>(.*?)</th>",
            table,
            flags=re.IGNORECASE | re.DOTALL,
        )
        if not header_match:
            continue
        risk = strip_tags(header_match.group(1))
        name = strip_tags(header_match.group(2))
        rows = re.findall(r"<tr\b[^>]*>(.*?)</tr>", table, flags=re.IGNORECASE | re.DOTALL)
        description = ""
        solution = ""
        current: dict[str, str] | None = None

        def flush_current() -> None:
            if not current or not current.get("URL"):
                return
            alerts.append(
                Alert(
                    name=name,
                    risk=risk,
                    confidence="",
                    method=current.get("Method", ""),
                    url=current.get("URL", ""),
                    parameter=current.get("Parameter", ""),
                    evidence=current.get("Evidence", ""),
                    solution=solution,
                    description=description,
                )
            )

        for row in rows:
            cells = re.findall(r"<t[dh]\b[^>]*>(.*?)</t[dh]>", row, flags=re.IGNORECASE | re.DOTALL)
            if len(cells) < 2:
                continue
            label = strip_tags(cells[0])
            value = strip_tags(cells[1])
            if label == "Description":
                description = value
                continue
            if label == "Solution":
                solution = value
                continue
            if label == "URL":
                flush_current()
                current = {"URL": value}
                continue
            if current is not None and label in {"Method", "Parameter", "Evidence"}:
                current[label] = value
        flush_current()
    return alerts


def dedupe_alerts(alerts: list[Alert]) -> list[Alert]:
    seen: set[tuple[str, str, str, str, str]] = set()
    result: list[Alert] = []
    for alert in sorted(alerts, key=lambda item: (RISK_ORDER.get(item.risk, 9), item.name, item.url)):
        key = (alert.name, alert.risk, alert.method, alert.url, alert.parameter)
        if key in seen:
            continue
        seen.add(key)
        result.append(alert)
    return result


def parse_zap_html(report_html: str) -> list[Alert]:
    alerts = parse_details_sections(report_html)
    alerts.extend(parse_classic_results(report_html))
    alerts.extend(parse_table_rows(report_html))
    return dedupe_alerts(alerts)


def load_dotenv(env_path: Path | None = None) -> None:
    candidate = env_path or SCRIPT_DIR / ".env"
    if not candidate.exists():
        return
    for line in candidate.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def find_default_report(input_dir: Path) -> Path:
    candidates = sorted(input_dir.glob("*.html"), key=lambda path: path.stat().st_mtime, reverse=True)
    if candidates:
        return candidates[0]
    root_report = Path("zap_report.html")
    if root_report.exists():
        return root_report
    raise FileNotFoundError(f"No ZAP HTML report found in {input_dir} or ./zap_report.html")


def summarize_alerts(alerts: list[Alert], limit: int) -> str:
    lines = []
    for index, alert in enumerate(alerts[:limit], start=1):
        fields = [
            f"{index}. {alert.risk} - {alert.name}",
            f"   URL: {alert.method} {alert.url}".rstrip(),
        ]
        if alert.confidence:
            fields.append(f"   Confidence: {alert.confidence}")
        if alert.parameter:
            fields.append(f"   Parameter: {alert.parameter}")
        if alert.evidence:
            fields.append(f"   Evidence: {alert.evidence[:500]}")
        if alert.solution:
            fields.append(f"   ZAP solution: {alert.solution[:500]}")
        lines.extend(fields)
    return "\n".join(lines)


def build_prompt(alerts: list[Alert], source_name: str, limit: int) -> str:
    alert_summary = summarize_alerts(alerts, limit=limit)
    return textwrap.dedent(
        f"""
        Bạn là security testing assistant cho seminar T09 Security Testing.
        Hãy đọc các alert OWASP ZAP dưới đây và viết phần AI-Triage cho Zap track bằng tiếng Việt.

        Yêu cầu output markdown:
        1. Ưu tiên triage theo risk và khả năng tái lập.
        2. Với mỗi finding quan trọng, ghi: ZAP Alert Note, nhận định thật/false positive, impact, PoC/reproducer, testcase, expected/actual result, fix suggestion.
        3. Nếu alert có vẻ do môi trường development như Vite dev server, ghi rõ là false positive/noise cần scan lại production build.
        4. Phần PoC chỉ dùng cho localhost/lab EShop, không hướng dẫn tấn công hệ thống bên ngoài.
        5. Thêm Human Audit Checklist để nhóm kiểm chứng output AI.
        6. Thêm Metrics/Failure Modes ngắn cho M3/M5.

        Source report: {source_name}

        ZAP alerts:
        {alert_summary}
        """
    ).strip()


def call_gemini(prompt: str, api_key: str, model: str, timeout: int = 20) -> str:
    url = GEMINI_ENDPOINT.format(model=model, api_key=api_key)
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2, "topP": 0.8},
    }
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "ignore")
        detail = body.strip() or str(exc)
        raise RuntimeError(f"Gemini API error {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error while calling Gemini: {exc.reason}") from exc
    except TimeoutError as exc:
        raise RuntimeError(f"Gemini request timed out after {timeout}s") from exc

    try:
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except (KeyError, IndexError) as exc:
        raise RuntimeError(f"Unexpected Gemini response: {data}") from exc


def classify_noise(alert: Alert) -> bool:
    dev_markers = ("/@vite", "/node_modules/.vite/", "vite-hmr", "@react-refresh")
    return any(marker in alert.url for marker in dev_markers) or any(marker in alert.evidence for marker in dev_markers)


def build_poc(alert: Alert) -> str:
    lower_name = alert.name.lower()
    if "cross site scripting" in lower_name or "xss" in lower_name:
        return textwrap.dedent(
            f"""
            **PoC DOM XSS**
            1. Mở trình duyệt tại `{alert.url}`.
            2. Nếu app có ô nhập tương ứng, nhập lại payload từ URL/evidence.
            3. Quan sát popup `alert(...)` hoặc DOM bị chèn thẻ HTML.

            **Testcase**
            - Input: `{alert.parameter or "query/hash payload"}`
            - Expected: payload được render như text an toàn, không chạy JavaScript.
            - Actual theo ZAP: payload có thể kích hoạt script trong browser.
            """
        ).strip()
    if "cross-domain" in lower_name or "cors" in lower_name:
        return textwrap.dedent(
            f"""
            **PoC CORS**
            1. Gửi request đến `{alert.url}` với header `Origin: http://evil.example`.
            2. Kiểm tra response header.

            **Testcase**
            - Expected: backend chỉ cho phép origin tin cậy như frontend EShop.
            - Actual theo ZAP: response có bằng chứng `{alert.evidence or "Access-Control-Allow-Origin quá rộng"}`.
            """
        ).strip()
    if "content security policy" in lower_name or "clickjacking" in lower_name or "content-type-options" in lower_name:
        return textwrap.dedent(
            f"""
            **PoC Security Header**
            1. Gửi `curl -I {alert.url}`.
            2. Kiểm tra header bảo vệ liên quan.

            **Testcase**
            - Expected: response có CSP/frame-ancestors hoặc `X-Content-Type-Options: nosniff` tùy finding.
            - Actual theo ZAP: header bị thiếu hoặc chưa đạt yêu cầu.
            """
        ).strip()
    return textwrap.dedent(
        f"""
        **PoC/Reproducer**
        1. Gửi request `{alert.method} {alert.url}` trong môi trường lab.
        2. So sánh response header/body với evidence của ZAP.

        **Testcase**
        - Expected: không xuất hiện evidence rủi ro.
        - Actual theo ZAP: `{alert.evidence or alert.name}`.
        """
    ).strip()


def build_offline_triage(alerts: list[Alert], source_name: str) -> str:
    if not alerts:
        return "Không trích xuất được alert nào từ report. Cần kiểm tra lại định dạng report hoặc chạy lại ZAP."

    sections = [
        "## AI Triage Note",
        f"Nguồn dữ liệu: `{source_name}`. Bản này dùng offline template vì chưa gọi AI hoặc AI không khả dụng.",
        "",
        "### Ưu tiên xử lý",
    ]
    for alert in alerts[:8]:
        noise_note = " Có dấu hiệu noise do dev server, nên xác nhận lại bằng production build." if classify_noise(alert) else ""
        title = f"#### {alert.risk} - {alert.name}"
        details = [
            title,
            f"- ZAP Alert Note: `{alert.method} {alert.url}`",
            f"- Confidence: {alert.confidence or 'N/A'}",
            f"- Parameter: {alert.parameter or 'N/A'}",
            f"- Evidence: {alert.evidence or 'N/A'}",
            f"- Triage: {'Cần reproduce thủ công.' if not classify_noise(alert) else 'Có khả năng false positive/noise.'}{noise_note}",
            f"- Impact: {impact_for(alert)}",
            "",
            build_poc(alert),
            "",
            f"- Fix suggestion: {fix_for(alert)}",
            "",
        ]
        sections.extend(details)
    sections.extend(
        [
            "### Human Audit Checklist",
            "- Đối chiếu URL/request trong ZAP với app EShop đang chạy.",
            "- Reproduce lại finding trên localhost và ghi screenshot/log.",
            "- Kiểm tra source code hoặc cấu hình server tương ứng trước khi kết luận fix.",
            "- Đánh dấu false positive nếu finding chỉ xuất hiện trên Vite/dev dependency.",
            "",
            "### Metrics / Failure Modes",
            "- Metrics cần ghi: thời gian scan, số alert theo risk, số finding reproduce được.",
            "- Failure mode 1: ZAP có thể báo security header thiếu trên dev server thay vì production server.",
            "- Failure mode 2: AI có thể viết PoC/fix quá chung, cần kiểm chứng bằng request/response thật.",
            "- Failure mode 3: Nếu ZAP thiếu auth context, các endpoint sau đăng nhập có thể bị bỏ sót.",
        ]
    )
    return "\n".join(sections)


def impact_for(alert: Alert) -> str:
    name = alert.name.lower()
    if "xss" in name or "cross site scripting" in name:
        return "Có thể thực thi JavaScript trong browser nạn nhân, đánh cắp dữ liệu phiên hoặc thao tác thay người dùng."
    if "cross-domain" in name or "cors" in name:
        return "Origin không tin cậy có thể đọc dữ liệu API nếu endpoint trả dữ liệu nhạy cảm hoặc được bảo vệ bằng mạng nội bộ."
    if "content security policy" in name:
        return "Thiếu lớp giảm thiểu XSS/data injection, làm tăng blast radius khi có bug injection."
    if "clickjacking" in name:
        return "Trang có thể bị nhúng iframe để lừa người dùng click thao tác ngoài ý muốn."
    if "x-powered-by" in name:
        return "Lộ fingerprint framework, hỗ trợ attacker chọn payload theo stack."
    return "Cần đánh giá theo evidence và dữ liệu endpoint trả về."


def fix_for(alert: Alert) -> str:
    name = alert.name.lower()
    if "xss" in name or "cross site scripting" in name:
        return "Không dùng `innerHTML` với input/query/hash; render text bằng React escaping mặc định; sanitize nếu bắt buộc render HTML."
    if "cross-domain" in name or "cors" in name:
        return "Giới hạn `Access-Control-Allow-Origin` theo allowlist frontend, không dùng `*` cho API có dữ liệu nghiệp vụ."
    if "content security policy" in name:
        return "Thêm CSP tối thiểu: `default-src 'self'; script-src 'self'; object-src 'none'; frame-ancestors 'none'` và điều chỉnh cho asset hợp lệ."
    if "clickjacking" in name:
        return "Thêm `Content-Security-Policy: frame-ancestors 'none'` hoặc `X-Frame-Options: DENY`."
    if "content-type-options" in name:
        return "Thêm `X-Content-Type-Options: nosniff` trên mọi response."
    if "x-powered-by" in name:
        return "Trong Express, gọi `app.disable('x-powered-by')`."
    return alert.solution or "Áp dụng khuyến nghị ZAP và kiểm chứng lại bằng scan."


def render_markdown(alerts: list[Alert], triage_text: str, source_name: str, model_name: str) -> str:
    counts: dict[str, int] = {}
    for alert in alerts:
        counts[alert.risk] = counts.get(alert.risk, 0) + 1
    counts_lines = "\n".join(f"- {risk}: {counts[risk]}" for risk in sorted(counts, key=lambda risk: RISK_ORDER.get(risk, 9)))
    alert_table = "\n".join(
        f"| {alert.risk} | {alert.confidence or 'N/A'} | {alert.name} | `{alert.method} {alert.url}` |"
        for alert in alerts[:12]
    )
    submission_block = build_submission_block(alerts, source_name=source_name)
    parts = [
        "# ZAP AI Triage Report",
        "",
        f"- Source report: `{source_name}`",
        f"- AI/model mode: `{model_name}`",
        f"- Alerts parsed: `{len(alerts)}`",
        "",
        "## Risk Summary",
        "",
        counts_lines or "- No alerts parsed",
        "",
        "## Parsed Alerts",
        "",
        "| Risk | Confidence | Alert | Request |",
        "| --- | --- | --- | --- |",
        alert_table or "| N/A | N/A | No parsed alerts | N/A |",
        "",
        triage_text,
        "",
        "## Submission Block",
        "",
        "Dán phần này vào `submission/Team_Work_Assignment.md` dưới Track B - ZAP flow hoặc Pha 2:",
        "",
        "```markdown",
        submission_block,
        "```",
        "",
    ]
    return "\n".join(parts)


def build_submission_block(alerts: list[Alert], source_name: str) -> str:
    counts: dict[str, int] = {}
    for alert in alerts:
        counts[alert.risk] = counts.get(alert.risk, 0) + 1
    counts_lines = "\n".join(f"- {risk}: {counts[risk]}" for risk in sorted(counts, key=lambda risk: RISK_ORDER.get(risk, 9)))
    high_or_first = next((alert for alert in alerts if alert.risk == "High"), alerts[0] if alerts else None)
    poc = build_poc(high_or_first) if high_or_first else "Chưa có alert để tạo PoC."
    return "\n".join(
        [
            "### AI-Triage cho ZAP Track",
            "",
            f"- Input: `{source_name}`",
            "- Tool: OWASP ZAP report + Gemini/offline AI triage script `docs/zap/ai_triage_zap.py`",
            f"- Tổng alert đã parse: {len(alerts)}",
            counts_lines or "- Không parse được alert.",
            "",
            "Kết quả triage chính:",
            compact_submission_summary(alerts),
            "",
            "PoC/reproducer ưu tiên:",
            poc,
            "",
            "Testcase/evidence cần nộp:",
            "- ZAP report gốc trong `docs/zap/output` hoặc `zap_report.html`.",
            "- AI triage output trong `docs/zap/ai_triage_output.md`.",
            "- Screenshot/log khi reproduce finding ưu tiên cao nhất.",
            "- Human audit note: AI chỉ hỗ trợ draft; nhóm kiểm chứng bằng request/response thật và source/runtime evidence.",
            "",
            "Failure modes quan sát được:",
            "- ZAP có thể báo noise trên Vite/dev server, ví dụ dependency trong `/node_modules/.vite` hoặc `@react-refresh`.",
            "- AI có thể gợi ý fix quá chung; cần đối chiếu source code/backend config.",
            "- Nếu ZAP không có auth context, scan có thể bỏ sót endpoint sau đăng nhập.",
        ]
    )


def compact_submission_summary(alerts: list[Alert]) -> str:
    if not alerts:
        return "- Chưa parse được alert; cần kiểm tra lại report."
    lines = []
    for alert in alerts[:5]:
        lines.append(f"- `{alert.risk}` `{alert.name}` tại `{alert.url}`: {impact_for(alert)}")
    return "\n".join(lines)


def update_submission_file(path: Path, block: str) -> None:
    content = path.read_text(encoding="utf-8")
    managed = f"{SUBMISSION_START}\n{block.strip()}\n{SUBMISSION_END}"
    pattern = rf"{re.escape(SUBMISSION_START)}.*?{re.escape(SUBMISSION_END)}"
    if re.search(pattern, content, flags=re.DOTALL):
        content = re.sub(pattern, managed, content, flags=re.DOTALL)
    else:
        anchor = "## Pha 2 - Thực hiện end-to-end nhóm testcase"
        if anchor in content:
            content = content.replace(anchor, f"{managed}\n\n{anchor}", 1)
        else:
            content = content.rstrip() + "\n\n" + managed + "\n"
    path.write_text(content, encoding="utf-8")


def load_alerts(input_path: Path | None) -> tuple[Path, list[Alert]]:
    report_path = input_path or find_default_report(DEFAULT_INPUT_DIR)
    report_path = report_path if report_path.is_absolute() else (Path.cwd() / report_path).resolve()
    report_html = report_path.read_text(encoding="utf-8", errors="ignore")
    return report_path, parse_zap_html(report_html)


def resolve_output_path(report_path: Path, output_path: Path | None) -> Path:
    if output_path is not None:
        return output_path if output_path.is_absolute() else (Path.cwd() / output_path).resolve()

    report_name = report_path.stem
    return (report_path.parent / f"{report_name}_ai_triage.md").resolve()


def main() -> int:
    load_dotenv()

    parser = argparse.ArgumentParser(description="Generate AI triage markdown from OWASP ZAP HTML reports.")
    parser.add_argument("--input", type=Path, help="Path to a ZAP HTML report. Defaults to latest docs/zap/output/*.html.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help=f"Markdown output path. Default: {DEFAULT_OUTPUT}")
    parser.add_argument("--use-ai", action="store_true", help="Call Gemini. Without this flag, uses offline triage template.")
    parser.add_argument("--model", default=os.getenv("GEMINI_MODEL", DEFAULT_MODEL), help=f"Gemini model. Default: {DEFAULT_MODEL}")
    parser.add_argument("--max-alerts", type=int, default=8, help="Maximum alerts to send to AI.")
    parser.add_argument("--update-submission", action="store_true", help=f"Update managed AI-Triage block in {DEFAULT_SUBMISSION}.")
    parser.add_argument("--submission-file", type=Path, default=DEFAULT_SUBMISSION, help=f"Submission markdown path. Default: {DEFAULT_SUBMISSION}")
    args = parser.parse_args()

    try:
        report_path, alerts = load_alerts(args.input)
    except OSError as exc:
        print(f"[!] Cannot read ZAP report: {exc}", file=sys.stderr)
        return 1

    model_name = "offline-template"
    triage_text = ""
    if args.use_ai:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("[!] GEMINI_API_KEY is not set. Falling back to offline triage.", file=sys.stderr)
        else:
            try:
                prompt = build_prompt(alerts, source_name=str(report_path), limit=args.max_alerts)
                triage_text = call_gemini(prompt, api_key=api_key, model=args.model)
                model_name = args.model
            except KeyboardInterrupt:
                print("[!] Gemini request interrupted. Falling back to offline triage.", file=sys.stderr)
            except (urllib.error.URLError, TimeoutError, RuntimeError, json.JSONDecodeError) as exc:
                print(f"[!] Gemini call failed: {exc}. Falling back to offline triage.", file=sys.stderr)

    if not triage_text:
        triage_text = build_offline_triage(alerts, source_name=str(report_path))

    output_path = resolve_output_path(report_path, args.output if args.output != DEFAULT_OUTPUT else None)

    markdown = render_markdown(alerts, triage_text, source_name=str(report_path), model_name=model_name)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")
    print(f"[+] Parsed {len(alerts)} alerts from {report_path}")
    print(f"[+] Wrote triage markdown to {output_path}")
    if args.update_submission:
        update_submission_file(args.submission_file, build_submission_block(alerts, source_name=str(report_path)))
        print(f"[+] Updated submission block in {args.submission_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
