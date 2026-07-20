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
DEFAULT_MODEL = "google/gemini-2.5-flash"
DEFAULT_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_TIMEOUT = 60
DEFAULT_MAX_TOKENS = 4096


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
    api_key: str
    model: str
    base_url: str
    timeout: int
    max_tokens: int


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
    api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is required in environment or src/zap/.env")
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
    return OpenRouterConfig(
        api_key=api_key,
        model=os.getenv("OPENROUTER_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL,
        base_url=os.getenv("OPENROUTER_BASE_URL", DEFAULT_BASE_URL).strip() or DEFAULT_BASE_URL,
        timeout=timeout,
        max_tokens=max_tokens,
    )


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
    notes = "Replay the request and compare the response with ZAP evidence."
    if parameter and attack:
        notes = f"Use parameter `{parameter}` with the ZAP attack payload, then inspect the response."
    elif method == "GET" and "cors" not in endpoint.lower():
        notes = "Replay the GET request and inspect response headers/body."
    elif request_body:
        notes = "Replay the request body captured by ZAP and inspect response behavior."
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
        "Hãy trích xuất TOÀN BỘ alert instances trong JSON input và viết report tiếng Việt.\n\n"
        "Yêu cầu format Markdown:\n"
        "- Mỗi alert instance là một mục riêng.\n"
        "- Mỗi mục phải có: Chi tiết + giải thích lỗi.\n"
        "- Mỗi mục phải có: Tag OWASP nếu có, tập trung vào mapping OWASP Top 10.\n"
        "- Mỗi mục phải có: PoC gồm method + endpoint + payload để validate lại bằng Postman.\n"
        "- Mỗi mục phải có: Cách verify PoC, gồm expected/actual và header/body cần kiểm tra.\n"
        "- Nếu finding có vẻ là noise/dev-server, vẫn ghi lại nhưng đánh dấu cần xác minh.\n"
        "- Chỉ hướng dẫn kiểm chứng trên localhost/lab; không mở rộng thành hướng dẫn tấn công hệ thống ngoài.\n\n"
        f"Source files: {', '.join(source_names)}\n\n"
        "ZAP alert instances JSON:\n"
        f"{json.dumps(payload, ensure_ascii=False, indent=2)}"
    )


def call_openrouter(prompt: str, config: OpenRouterConfig) -> str:
    body = {
        "model": config.model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "top_p": 0.8,
        "max_tokens": config.max_tokens,
    }
    request = urllib.request.Request(
        config.base_url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config.api_key}",
            "HTTP-Referer": "https://github.com",
            "X-Title": "ZAP OpenRouter JSON Extract",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=config.timeout) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "ignore").strip()
        raise RuntimeError(f"OpenRouter API error {exc.code}: {detail or exc.reason}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error while calling OpenRouter: {exc.reason}") from exc
    except TimeoutError as exc:
        raise RuntimeError(f"OpenRouter request timed out after {config.timeout}s") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError("OpenRouter returned a non-JSON response") from exc

    try:
        return str(data["choices"][0]["message"]["content"]).strip()
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError(f"Unexpected OpenRouter response: {data}") from exc


def render_markdown(ai_text: str, source_names: list[str], model: str) -> str:
    return "\n".join(
        [
            "# ZAP OpenRouter JSON Extract Result",
            "",
            f"- Source files: `{', '.join(source_names)}`",
            f"- OpenRouter model: `{model}`",
            "",
            ai_text.strip(),
            "",
        ]
    )


def render_html(ai_text: str, source_names: list[str], model: str) -> str:
    escaped_text = html.escape(ai_text.strip())
    escaped_sources = html.escape(", ".join(source_names))
    escaped_model = html.escape(model)
    return "\n".join(
        [
            "<!doctype html>",
            '<html lang="vi">',
            "<head>",
            '  <meta charset="utf-8">',
            "  <title>ZAP OpenRouter JSON Extract Result</title>",
            "  <style>",
            "    body { font-family: system-ui, sans-serif; line-height: 1.55; margin: 32px; max-width: 1100px; }",
            "    pre { white-space: pre-wrap; background: #f6f8fa; padding: 16px; border-radius: 6px; }",
            "    code { background: #f6f8fa; padding: 2px 4px; border-radius: 4px; }",
            "  </style>",
            "</head>",
            "<body>",
            "  <h1>ZAP OpenRouter JSON Extract Result</h1>",
            f"  <p><strong>Source files:</strong> <code>{escaped_sources}</code></p>",
            f"  <p><strong>OpenRouter model:</strong> <code>{escaped_model}</code></p>",
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


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    input_paths = [Path(value) for value in args.input]
    output_path = Path(args.output)

    try:
        config = config_from_env()
        alerts = parse_zap_json_files(input_paths)
        if not alerts:
            raise RuntimeError("No ZAP alert instances were found in the input JSON file(s)")
        source_names = [path.name for path in input_paths]
        prompt = build_prompt(alerts, source_names)
        ai_text = call_openrouter(prompt, config)
        if args.format == "markdown":
            output_text = render_markdown(ai_text, source_names, config.model)
        else:
            output_text = render_html(ai_text, source_names, config.model)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output_text, encoding="utf-8")
    except Exception as exc:
        print(f"[!] {exc}", file=sys.stderr)
        return 1

    print(f"[+] Wrote OpenRouter ZAP extraction report: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
