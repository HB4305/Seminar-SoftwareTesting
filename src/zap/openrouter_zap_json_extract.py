#!/usr/bin/env python3
"""Extract OWASP ZAP JSON alerts with OpenRouter/Gemini.

Usage:
    python src/zap/openrouter_zap_json_extract.py \
      --input src/zap/output/backend_basic.json \
      --format markdown \
      --output src/zap/output/zap_openrouter_result.md
"""

from __future__ import annotations

import argparse
import dataclasses
import html
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_ENV_PATH = SCRIPT_DIR / ".env"
DEFAULT_OPENROUTER_MODEL = "google/gemini-2.5-flash"
DEFAULT_OPENAI_MODEL = "gpt-4o-mini"
DEFAULT_OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_OPENAI_BASE_URL = "https://api.openai.com/v1/chat/completions"
DEFAULT_TIMEOUT = 60
DEFAULT_MAX_TOKENS = 1800
OPENROUTER_MAX_TOKENS_RE = re.compile(r"can only afford\s+(\d+)", re.IGNORECASE)


@dataclasses.dataclass(frozen=True)
class ExtractedAlert:
    source_file: str
    site: str
    alert_name: str
    risk: str
    confidence: str
    method: str
    endpoint: str
    parameter: str
    attack: str
    evidence: str
    description: str
    solution: str
    owasp_tags: list[str]
    request_header: str
    request_body: str
    response_header: str
    response_body: str
    poc: dict[str, str]


@dataclasses.dataclass(frozen=True)
class OpenRouterConfig:
    provider: str
    api_key: str
    model: str
    base_url: str
    timeout: int
    max_tokens: int


def provider_display_name(provider: str) -> str:
    if provider == "openai":
        return "OpenAI"
    if provider == "openrouter":
        return "OpenRouter"
    return provider


def extract_openrouter_affordable_max_tokens(detail: str) -> int | None:
    match = OPENROUTER_MAX_TOKENS_RE.search(detail)
    if not match:
        return None
    try:
        value = int(match.group(1))
    except ValueError:
        return None
    return value if value > 0 else None


def strip_html(value: str) -> str:
    text = re.sub(r"<br\s*/?>", "\n", str(value), flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r"\n\s+", "\n", text)
    return text.strip()


def load_dotenv(env_path: Path = DEFAULT_ENV_PATH) -> None:
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def config_from_env(env_path: Path = DEFAULT_ENV_PATH) -> OpenRouterConfig:
    load_dotenv(env_path)
    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    openrouter_key = os.getenv("OPENROUTER_API_KEY", "").strip()

    timeout_raw = os.getenv("OPENROUTER_TIMEOUT", str(DEFAULT_TIMEOUT)).strip()
    max_tokens_raw = os.getenv("OPENROUTER_MAX_TOKENS", str(DEFAULT_MAX_TOKENS)).strip()
    try:
        timeout = int(timeout_raw)
    except ValueError as exc:
        raise RuntimeError("OPENROUTER_TIMEOUT must be an integer number of seconds") from exc
    try:
        max_tokens = int(max_tokens_raw)
    except ValueError as exc:
        raise RuntimeError("OPENROUTER_MAX_TOKENS must be an integer") from exc
    if max_tokens <= 0:
        raise RuntimeError("OPENROUTER_MAX_TOKENS must be greater than zero")

    if openai_key:
        return OpenRouterConfig(
            provider="openai",
            api_key=openai_key,
            model=os.getenv("OPENAI_MODEL", DEFAULT_OPENAI_MODEL).strip() or DEFAULT_OPENAI_MODEL,
            base_url=os.getenv("OPENAI_BASE_URL", DEFAULT_OPENAI_BASE_URL).strip() or DEFAULT_OPENAI_BASE_URL,
            timeout=timeout,
            max_tokens=max_tokens,
        )

    if openrouter_key:
        return OpenRouterConfig(
            provider="openrouter",
            api_key=openrouter_key,
            model=os.getenv("OPENROUTER_MODEL", DEFAULT_OPENROUTER_MODEL).strip() or DEFAULT_OPENROUTER_MODEL,
            base_url=os.getenv("OPENROUTER_BASE_URL", DEFAULT_OPENROUTER_BASE_URL).strip() or DEFAULT_OPENROUTER_BASE_URL,
            timeout=timeout,
            max_tokens=max_tokens,
        )

    raise RuntimeError("Set OPENAI_API_KEY or OPENROUTER_API_KEY in environment or src/zap/.env")


def parse_zap_json_files(paths: list[Path]) -> list[ExtractedAlert]:
    alerts: list[ExtractedAlert] = []
    for path in paths:
        if not path.exists():
            raise FileNotFoundError(f"ZAP JSON input not found: {path}")
        try:
            report = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid ZAP JSON file {path}: {exc}") from exc
        alerts.extend(parse_zap_report(report, source_file=path.name))
    return alerts


def parse_zap_report(report: dict[str, Any], source_file: str) -> list[ExtractedAlert]:
    extracted: list[ExtractedAlert] = []
    sites = report.get("site", [])
    if isinstance(sites, dict):
        sites = [sites]
    if not isinstance(sites, list):
        return extracted

    for site in sites:
        if not isinstance(site, dict):
            continue
        site_name = str(site.get("@name", ""))
        site_name_lower = site_name.lower()
        if "localhost" not in site_name_lower and "127.0.0.1" not in site_name_lower:
            continue
        alerts = site.get("alerts", [])
        if isinstance(alerts, dict):
            alerts = [alerts]
        if not isinstance(alerts, list):
            continue
        for alert in alerts:
            if not isinstance(alert, dict):
                continue
            owasp_tags = extract_owasp_tags(alert.get("tags"))
            risk, confidence = split_risk_confidence(alert)
            if risk.lower() in {"informational", "info"}:
                continue
            instances = alert.get("instances", [])
            if isinstance(instances, dict):
                instances = [instances]
            if not isinstance(instances, list):
                instances = []
            for instance in instances:
                if not isinstance(instance, dict):
                    continue
                endpoint = str(instance.get("uri", ""))
                if not endpoint:
                    continue
                method = str(instance.get("method", "GET")).upper()
                parameter = str(instance.get("param", ""))
                attack = str(instance.get("attack", ""))
                request_body = str(instance.get("request-body", ""))
                poc = build_poc_fields(method, endpoint, parameter, attack, request_body)
                extracted.append(
                    ExtractedAlert(
                        source_file=source_file,
                        site=site_name,
                        alert_name=str(alert.get("alert") or alert.get("name") or "Unknown Alert"),
                        risk=risk,
                        confidence=str(alert.get("confidence") or confidence),
                        method=method,
                        endpoint=endpoint,
                        parameter=parameter,
                        attack=attack,
                        evidence=str(instance.get("evidence", "")),
                        description=strip_html(str(alert.get("desc", ""))),
                        solution=strip_html(str(alert.get("solution", ""))),
                        owasp_tags=owasp_tags,
                        request_header=str(instance.get("request-header", "")),
                        request_body=request_body,
                        response_header=str(instance.get("response-header", "")),
                        response_body=str(instance.get("response-body", "")),
                        poc=poc,
                    )
                )
    return extracted


def split_risk_confidence(alert: dict[str, Any]) -> tuple[str, str]:
    riskdesc = str(alert.get("riskdesc", "")).strip()
    if not riskdesc:
        return str(alert.get("risk", "Unknown") or "Unknown"), str(alert.get("confidence", ""))
    match = re.match(r"^([^(]+?)(?:\s*\(([^)]+)\))?$", riskdesc)
    if not match:
        return riskdesc, str(alert.get("confidence", ""))
    risk = match.group(1).strip() or "Unknown"
    confidence = match.group(2).strip() if match.group(2) else str(alert.get("confidence", ""))
    return risk, confidence


def extract_owasp_tags(raw_tags: Any) -> list[str]:
    tags: list[str] = []
    if isinstance(raw_tags, dict):
        tags = [str(key) for key in raw_tags.keys()]
    elif isinstance(raw_tags, list):
        for item in raw_tags:
            if isinstance(item, dict):
                tag = item.get("tag") or item.get("name")
                if tag:
                    tags.append(str(tag))
            elif item:
                tags.append(str(item))
    elif isinstance(raw_tags, str) and raw_tags.strip():
        tags = [part.strip() for part in raw_tags.split(",") if part.strip()]
    unique_tags = list(dict.fromkeys(tags))
    return [tag for tag in unique_tags if "owasp" in tag.lower()]


def build_poc_fields(
    method: str,
    endpoint: str,
    parameter: str,
    attack: str,
    request_body: str,
) -> dict[str, str]:
    method = method.upper()
    payload = attack or request_body
    notes = "Replay the request and compare the real EShop response with ZAP evidence."
    if parameter and attack:
        notes = (
            f"Use parameter `{parameter}` with the ZAP attack payload, then inspect the real EShop "
            "response headers/body before concluding the vulnerability."
        )
    elif method == "GET" and "cors" not in endpoint.lower():
        notes = "Replay the GET request and inspect the real EShop response headers/body."
    elif request_body:
        notes = "Replay the request body captured by ZAP and inspect the real EShop response behavior."
    return {
        "method": method,
        "endpoint": endpoint,
        "payload": payload,
        "notes": notes,
    }


def alert_to_prompt_dict(alert: ExtractedAlert) -> dict[str, Any]:
    return {
        "source_file": alert.source_file,
        "site": alert.site,
        "alert": alert.alert_name,
        "risk": alert.risk,
        "confidence": alert.confidence,
        "details": {
            "description": alert.description,
            "evidence": alert.evidence,
            "solution_from_zap": alert.solution,
        },
        "tags": {
            "owasp": alert.owasp_tags,
        },
        "poc": alert.poc,
        "request": {
            "request_line": f"{alert.method} {alert.endpoint}".strip(),
            "method": alert.method,
            "endpoint": alert.endpoint,
            "parameter": alert.parameter,
            "attack": alert.attack,
            "request_header": alert.request_header[:1200],
            "request_body": alert.request_body[:1200],
            "response_header": alert.response_header[:1200],
            "response_body": alert.response_body[:1200],
        },
    }


def build_prompt(alerts: list[ExtractedAlert], source_names: list[str]) -> str:
    payload = [alert_to_prompt_dict(alert) for alert in alerts]
    return (
        "Bạn là security testing assistant cho seminar DAST OWASP ZAP.\n"
        "Hãy trích xuất các alert instances trong JSON input và viết report tiếng Việt.\n\n"
        "Yêu cầu QUAN TRỌNG: Viết cực kỳ ngắn gọn, súc tích, đi thẳng vào vấn đề. Tránh giải thích dài dòng.\n"
        "- Mỗi loại alert là một mục riêng.\n"
        "- Mỗi mục phải ghi rõ các thông tin tham chiếu (reference) chi tiết từ ZAP alert:\n"
        "  * **Nguồn phát hiện (Source)**: Tên file JSON nguồn chứa alert.\n"
        "  * **Độ nguy hiểm (Risk) & Độ tin cậy (Confidence)**.\n"
        "  * **Mô tả lỗ hổng (Vulnerability description)**: 1-2 câu ngắn, nêu bản chất lỗi.\n"
        "  * **Các URL bị ảnh hưởng (Affected URLs)**: Liệt kê các endpoint/URL bị lỗi (lấy từ thông tin 'bị ảnh hưởng bởi lỗi này' trong description).\n"
        "  * **PoC**: Method + endpoint + payload/query test; nếu chưa đủ thông tin, hãy yêu cầu PoC cụ thể.\n"
        "  * **Cách verify PoC**: Tối đa 2-3 câu ngắn ghi Expected/Actual và Header/Body cần check.\n"
        "  * **Xác nhận bằng phản hồi thật từ EShop**: Luôn đối chiếu với response_header/response_body thật từ EShop trước khi kết luận vulnerability. Nếu chưa có xác nhận từ phản hồi thật từ EShop, ghi chú rõ là chưa được xác nhận.\n"
        "- Nếu finding có vẻ là noise/dev-server, ghi chú ngắn 'Có thể là noise do dev server'.\n"
        "- Giới hạn tổng dung lượng phản hồi cực ngắn để tránh bị cắt cụt (truncation).\n\n"
        f"Source files: {', '.join(source_names)}\n\n"
        "ZAP alert instances JSON:\n"
        f"{json.dumps(payload, ensure_ascii=False, indent=2)}"
    )


def call_openrouter(prompt: str, config: OpenRouterConfig) -> str:
    return _call_provider(prompt, config)


def _call_provider(prompt: str, config: OpenRouterConfig) -> str:
    provider_name = provider_display_name(config.provider)
    body = {
        "model": config.model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "top_p": 0.8,
        "max_tokens": config.max_tokens,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config.api_key}",
    }
    if config.provider == "openrouter":
        headers.update(
            {
                "HTTP-Referer": "https://github.com",
                "X-Title": "ZAP OpenRouter JSON Extract",
            }
        )
    elif config.provider == "openai":
        headers["Accept"] = "application/json"

    request = urllib.request.Request(
        config.base_url,
        data=json.dumps(body).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=config.timeout) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "ignore").strip()
        if config.provider == "openrouter" and exc.code == 402:
            affordable_max_tokens = extract_openrouter_affordable_max_tokens(detail)
            if affordable_max_tokens is not None and affordable_max_tokens < config.max_tokens:
                retry_config = dataclasses.replace(config, max_tokens=affordable_max_tokens)
                return _call_provider(prompt, retry_config)
        raise RuntimeError(f"{provider_name} API error {exc.code}: {detail or exc.reason}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error while calling {provider_name}: {exc.reason}") from exc
    except TimeoutError as exc:
        raise RuntimeError(f"{provider_name} request timed out after {config.timeout}s") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"{provider_name} returned a non-JSON response") from exc

    try:
        content = data["choices"][0]["message"]["content"]
        if isinstance(content, list):
            content = "".join(part.get("text", "") for part in content if isinstance(part, dict))
        return str(content).strip()
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError(f"Unexpected {provider_name} response: {data}") from exc


def render_markdown(ai_text: str, source_names: list[str], model: str, provider: str = "openrouter") -> str:
    provider_name = provider_display_name(provider)
    return "\n".join(
        [
            f"# ZAP {provider_name} JSON Extract Result",
            "",
            f"- Source files: `{', '.join(source_names)}`",
            f"- {provider_name} model: `{model}`",
            "",
            ai_text.strip(),
            "",
        ]
    )


def render_html(ai_text: str, source_names: list[str], model: str, provider: str = "openrouter") -> str:
    provider_name = provider_display_name(provider)
    escaped_text = html.escape(ai_text.strip())
    escaped_sources = html.escape(", ".join(source_names))
    escaped_model = html.escape(model)
    escaped_provider = html.escape(provider_name)
    return "\n".join(
        [
            "<!doctype html>",
            '<html lang="vi">',
            "<head>",
            '  <meta charset="utf-8">',
            f"  <title>ZAP {escaped_provider} JSON Extract Result</title>",
            "  <style>",
            "    body { font-family: system-ui, sans-serif; line-height: 1.55; margin: 32px; max-width: 1100px; }",
            "    pre { white-space: pre-wrap; background: #f6f8fa; padding: 16px; border-radius: 6px; }",
            "    code { background: #f6f8fa; padding: 2px 4px; border-radius: 4px; }",
            "  </style>",
            "</head>",
            "<body>",
            f"  <h1>ZAP {escaped_provider} JSON Extract Result</h1>",
            f"  <p><strong>Source files:</strong> <code>{escaped_sources}</code></p>",
            f"  <p><strong>{escaped_provider} model:</strong> <code>{escaped_model}</code></p>",
            f"  <pre>{escaped_text}</pre>",
            "</body>",
            "</html>",
        ]
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Use OpenRouter/Gemini to extract PoC-ready findings from ZAP JSON reports."
    )
    parser.add_argument(
        "--input",
        nargs="+",
        required=True,
        help="One or more ZAP JSON report files.",
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "html"],
        required=True,
        help="Output format.",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output file path.",
    )
    return parser


def deduplicate_alerts(alerts: list[ExtractedAlert]) -> list[ExtractedAlert]:
    """Nhóm các alert trùng tên để tối ưu hóa token và tránh bị AI cut-off."""
    grouped: dict[str, list[ExtractedAlert]] = {}
    for alert in alerts:
        grouped.setdefault(alert.alert_name, []).append(alert)

    deduped: list[ExtractedAlert] = []
    for name, list_of_alerts in grouped.items():
        rep = list_of_alerts[0]
        endpoints = [f"`{a.method} {a.endpoint}`" for a in list_of_alerts]
        
        new_desc = (
            f"{rep.description}\n\n"
            f"**Các URL/endpoints bị ảnh hưởng bởi lỗi này:**\n"
        )
        new_desc += "\n".join(f"- {ep}" for ep in endpoints[:15])
        if len(endpoints) > 15:
            new_desc += f"\n- ... và {len(endpoints) - 15} endpoint khác."
            
        deduped.append(
            dataclasses.replace(rep, description=new_desc)
        )
    return deduped


LOCAL_TEMPLATES = {
    "CSP: Failure to Define Directive with No Fallback": {
        "desc": "Chính sách bảo mật nội dung (CSP) không định nghĩa các chỉ thị bắt buộc, có thể dẫn đến việc cho phép mọi thứ.",
        "expected": "Header `Content-Security-Policy` có các chỉ thị đầy đủ.",
        "actual": "Header `Content-Security-Policy: default-src 'none'` thiếu các chỉ thị khác.",
    },
    "Cross-Domain Misconfiguration": {
        "desc": "Cấu hình CORS cho phép `Access-Control-Allow-Origin: *`, có thể dẫn đến việc tải dữ liệu trình duyệt từ các miền không mong muốn.",
        "expected": "Header `Access-Control-Allow-Origin` chỉ cho phép các miền cụ thể.",
        "actual": "Header `Access-Control-Allow-Origin: *` trong phản hồi.",
    },
    "Server Leaks Information via \"X-Powered-By\" HTTP Response Header Field(s)": {
        "desc": "Header `X-Powered-By` tiết lộ thông tin về công nghệ máy chủ (`Express`), có thể giúp kẻ tấn công tìm kiếm lỗ hổng.",
        "expected": "Không có header `X-Powered-By` trong phản hồi.",
        "actual": "Header `X-Powered-By: Express` xuất hiện trong phản hồi.",
    },
    "Cross Site Scripting (DOM Based)": {
        "desc": "Ứng dụng dễ bị tấn công XSS dựa trên DOM, cho phép kẻ tấn công thực thi mã độc trong trình duyệt người dùng.",
        "expected": "Không có cửa sổ `alert` bật lên hoặc mã JavaScript không được thực thi.",
        "actual": "Cửa sổ `alert` bật lên trong trình duyệt khi truy cập URL.",
    },
    "Path Traversal": {
        "desc": "Ứng dụng có thể bị tấn công Path Traversal, cho phép truy cập các tệp và thư mục ngoài thư mục gốc của web.",
        "expected": "Không thể truy cập các tệp ngoài phạm vi cho phép hoặc nhận mã lỗi.",
        "actual": "Yêu cầu trả về nội dung của tệp tin nguồn.",
    },
    "Content Security Policy (CSP) Header Not Set": {
        "desc": "Header CSP không được thiết lập, thiếu lớp bảo mật chống XSS và các cuộc tấn công injection.",
        "expected": "Header `Content-Security-Policy` được thiết lập.",
        "actual": "Không có header `Content-Security-Policy` trong phản hồi.",
    },
    "Missing Anti-clickjacking Header": {
        "desc": "Phản hồi thiếu header chống Clickjacking (`X-Frame-Options` hoặc `Content-Security-Policy` với `frame-ancestors`).",
        "expected": "Header `X-Frame-Options` hoặc `Content-Security-Policy` với `frame-ancestors` được thiết lập.",
        "actual": "Không có các header chống Clickjacking trong phản hồi.",
    },
    "Timestamp Disclosure - Unix": {
        "desc": "Ứng dụng/máy chủ web tiết lộ dấu thời gian Unix, có thể cung cấp thông tin nhạy cảm cho kẻ tấn công.",
        "expected": "Không có dấu thời gian Unix hiển thị trong phản hồi.",
        "actual": "Giá trị dấu thời gian xuất hiện trong phản hồi.",
    },
    "X-Content-Type-Options Header Missing": {
        "desc": "Header `X-Content-Type-Options` không được đặt thành 'nosniff', cho phép MIME-sniffing.",
        "expected": "Header `X-Content-Type-Options: nosniff` được thiết lập.",
        "actual": "Không có header `X-Content-Type-Options` trong phản hồi.",
    }
}


def generate_local_report(alerts: list[ExtractedAlert], source_names: list[str]) -> str:
    lines = [
        "# ZAP OpenRouter JSON Extract Result",
        "",
        f"- Source files: `{', '.join(source_names)}`",
        "- Render Mode: `Local Security Triage Engine`",
        "",
        "Dưới đây là báo cáo các lỗ hổng bảo mật được trích xuất từ dữ liệu ZAP:",
        "",
        "---",
        ""
    ]
    
    for idx, alert in enumerate(alerts, 1):
        template = LOCAL_TEMPLATES.get(alert.alert_name, {})
        desc_parts = alert.description.split("\n\n**Các URL/endpoints bị ảnh hưởng bởi lỗi này:**\n")
        clean_desc = template.get("desc", desc_parts[0])
        expected = template.get("expected", "Không phát hiện cấu hình sai hoặc lỗ hổng.")
        actual = template.get("actual", f"Phát hiện dấu hiệu của: {alert.alert_name}")
        
        affected_section = desc_parts[1] if len(desc_parts) > 1 else f"- `{alert.method} {alert.endpoint}`"

        # Check if it could be noise
        noise_note = ""
        endpoint_lower = alert.endpoint.lower()
        if "localhost" not in endpoint_lower and "127.0.0.1" not in endpoint_lower:
            noise_note = "Có thể là noise do dev server."
        elif "node_modules" in endpoint_lower or "vite" in endpoint_lower:
            noise_note = "Có thể là noise do dev server."

        tags_str = ", ".join(alert.owasp_tags) if alert.owasp_tags else "N/A"
        
        lines.extend([
            f"### {idx}. {alert.alert_name}",
            f"- **Nguồn phát hiện (Source)**: `{alert.source_file}`",
            f"- **Độ nguy hiểm (Risk) & Độ tin cậy (Confidence)**: `{alert.risk}` & `{alert.confidence}`",
            f"- **Các URL bị ảnh hưởng (Affected URLs)**:",
            affected_section,
            f"- **Bản chất lỗi**: {clean_desc}",
            f"- **Tag OWASP**: {tags_str}",
            f"- **PoC**: `{alert.method} {alert.endpoint}`" + (f"?{alert.parameter}={alert.attack}" if alert.parameter and alert.attack else ""),
            f"- **Cách verify PoC**:",
            f"  * **Expected**: {expected}",
            f"  * **Actual**: {actual}",
        ])
        if noise_note:
            lines.append(f"- **Ghi chú**: {noise_note}")
        lines.extend([
            "",
            "---",
            ""
        ])
        
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    input_paths = [Path(value) for value in args.input]
    output_path = Path(args.output)

    try:
        config = config_from_env()
        alerts = parse_zap_json_files(input_paths)
        alerts = deduplicate_alerts(alerts)
        if not alerts:
            raise RuntimeError("No ZAP alert instances were found in the input JSON file(s)")
        source_names = [path.name for path in input_paths]
        
        try:
            prompt = build_prompt(alerts, source_names)
            ai_text = call_openrouter(prompt, config)
            if args.format == "markdown":
                output_text = render_markdown(ai_text, source_names, config.model, config.provider)
            else:
                output_text = render_html(ai_text, source_names, config.model, config.provider)
        except Exception as api_exc:
            provider_name = provider_display_name(config.provider)
            print(f"[*] {provider_name} API failed ({api_exc}). Falling back to local deterministic triager...", file=sys.stderr)
            output_text = generate_local_report(alerts, source_names)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output_text, encoding="utf-8")
    except Exception as exc:
        print(f"[!] {exc}", file=sys.stderr)
        return 1

    print(f"[+] Wrote {provider_display_name(config.provider)} ZAP extraction report: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
