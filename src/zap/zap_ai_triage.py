import argparse
import html
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, NamedTuple, Optional


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_OUTPUT_DIR = SCRIPT_DIR / "output"
DEFAULT_AI_MAX_TOKENS = 1800
MAX_EVIDENCE_CHARS = 4000


class AiSettings(NamedTuple):
    provider: str
    model: str
    api_key: str
    base_url: Optional[str] = None
    max_tokens: int = DEFAULT_AI_MAX_TOKENS


class ZapAlertRecord(NamedTuple):
    index: int
    alert_id: str
    source_json: str
    site: str
    plugin_id: str
    alert_ref: str
    alert_name: str
    risk: str
    confidence: str
    cwe: str
    wasc: str
    tags: str
    url: str
    method: str
    param: str
    attack: str
    evidence: str
    request_header: str
    request_body: str
    response_header: str
    response_body: str
    description: str
    solution: str
    reference: str


class ZapAlertGroup(NamedTuple):
    index: int
    alert_id: str
    records: List[ZapAlertRecord]


def configure_console_encoding(stdout=None, stderr=None):
    """Prefer UTF-8 output on terminals that support reconfigure()."""
    for stream in (stdout or sys.stdout, stderr or sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            try:
                reconfigure(encoding="utf-8")
            except Exception:
                pass


def load_env_file(env_file):
    if not env_file:
        return {}
    env_path = Path(env_file)
    if not env_path.exists():
        return {}

    values = {}
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def find_default_env_file():
    for candidate in (Path.cwd() / ".env", SCRIPT_DIR / ".env", SCRIPT_DIR / ".env.example"):
        if candidate.exists():
            return candidate
    return None


def get_ai_settings(env: Optional[Mapping[str, str]] = None, env_file=None):
    merged_env = {}
    default_env_file = find_default_env_file() if env_file is None else env_file
    merged_env.update(load_env_file(default_env_file))
    merged_env.update(dict(os.environ if env is None else env))

    provider = "openai-compatible"
    max_tokens_raw = (
        merged_env.get("AI_MAX_TOKENS")
        or merged_env.get("OPENROUTER_MAX_TOKENS")
        or str(DEFAULT_AI_MAX_TOKENS)
    )
    try:
        max_tokens = int(str(max_tokens_raw).strip())
    except ValueError as exc:
        raise ValueError("AI_MAX_TOKENS phải là số nguyên dương.") from exc
    if max_tokens <= 0:
        raise ValueError("AI_MAX_TOKENS phải là số nguyên dương.")

    openai_key = merged_env.get("OPENAI_API_KEY") or merged_env.get("AI_API_KEY")
    openrouter_key = merged_env.get("OPENROUTER_API_KEY")
    if openai_key:
        api_key = openai_key
        model = (
            merged_env.get("AI_MODEL")
            or merged_env.get("OPENAI_MODEL")
            or "gpt-4.1-mini"
        ).strip()
        base_url = normalize_openai_compatible_base_url(
            merged_env.get("OPENAI_BASE_URL") or "https://api.openai.com/v1"
        )
    elif openrouter_key:
        api_key = openrouter_key
        model = (
            merged_env.get("AI_MODEL")
            or merged_env.get("OPENROUTER_MODEL")
            or "google/gemini-2.5-flash"
        ).strip()
        base_url = normalize_openai_compatible_base_url(
            merged_env.get("OPENROUTER_BASE_URL") or "https://openrouter.ai/api/v1"
        )
    else:
        raise ValueError("Chưa thiết lập OPENAI_API_KEY hoặc OPENROUTER_API_KEY.")

    if not model:
        raise ValueError("Chưa thiết lập AI_MODEL cho provider đã chọn.")
    if not base_url:
        raise ValueError("Chưa thiết lập OPENROUTER_BASE_URL hoặc OPENAI_BASE_URL cho provider openai-compatible.")

    return AiSettings(provider, model, api_key, base_url, max_tokens)


def normalize_openai_compatible_base_url(base_url):
    normalized = str(base_url or "").strip().rstrip("/")
    suffix = "/chat/completions"
    if normalized.endswith(suffix):
        normalized = normalized[: -len(suffix)]
    return normalized.rstrip("/")


def strip_html(value):
    text = re.sub(r"<[^>]+>", "", value or "")
    return html.unescape(text).strip()


def normalize_text(value, fallback="N/A"):
    if value is None:
        return fallback
    text = str(value).strip()
    return text if text else fallback


def normalize_multiline(value):
    return str(value or "").replace("\r\n", "\n").strip()


def truncate_text(value, max_chars=MAX_EVIDENCE_CHARS):
    text = normalize_multiline(value)
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + "\n...[đã rút gọn]"


def parse_risk_and_confidence(alert):
    riskdesc = normalize_text(alert.get("riskdesc"), "Unknown")
    match = re.match(r"(?P<risk>[^()]+?)(?:\s*\((?P<confidence>[^()]+)\))?$", riskdesc)
    if not match:
        return riskdesc, normalize_text(alert.get("confidence"), "Unknown")
    risk = match.group("risk").strip() or "Unknown"
    confidence = (match.group("confidence") or "").strip()
    if not confidence:
        confidence = normalize_text(alert.get("confidence"), "Unknown")
    return risk, confidence


def normalize_cwe(value):
    text = normalize_text(value)
    if text in {"N/A", "-1", "0"}:
        return "N/A"
    return f"CWE-{text}" if not str(text).upper().startswith("CWE-") else str(text)


def normalize_wasc(value):
    text = normalize_text(value)
    if text in {"N/A", "-1", "0"}:
        return "N/A"
    return f"WASC-{text}" if not str(text).upper().startswith("WASC-") else str(text)


def normalize_tags(tags):
    if not tags:
        return "N/A"
    values = []
    for tag in tags:
        if isinstance(tag, dict):
            value = tag.get("tag") or tag.get("name") or tag.get("key")
        else:
            value = tag
        if value:
            values.append(str(value))
    return ", ".join(values) if values else "N/A"


def url_matches_prefixes(url, target_prefixes):
    if not target_prefixes:
        return True
    return any(str(url or "").startswith(prefix) for prefix in target_prefixes)


def collect_alert_records(
    zap_data: Mapping,
    source_json: str,
    start_index: int = 1,
    target_prefixes: Optional[Iterable[str]] = None,
):
    records = []
    next_index = start_index
    prefixes = [prefix for prefix in (target_prefixes or []) if prefix]

    for site in zap_data.get("site", []) or []:
        site_name = normalize_text(site.get("@name"), "N/A")
        for alert in site.get("alerts", []) or []:
            risk, confidence = parse_risk_and_confidence(alert)
            instances = alert.get("instances") or [{}]
            for instance in instances:
                url = normalize_text(instance.get("uri") or instance.get("nodeName"), "N/A")
                if not url_matches_prefixes(url, prefixes):
                    continue
                alert_id = f"ZAP-{next_index:03d}"
                records.append(
                    ZapAlertRecord(
                        index=next_index,
                        alert_id=alert_id,
                        source_json=source_json,
                        site=site_name,
                        plugin_id=normalize_text(alert.get("pluginid"), "N/A"),
                        alert_ref=normalize_text(alert.get("alertRef"), normalize_text(alert.get("pluginid"), "N/A")),
                        alert_name=normalize_text(alert.get("alert") or alert.get("name"), "Unknown Alert"),
                        risk=risk,
                        confidence=confidence,
                        cwe=normalize_cwe(alert.get("cweid")),
                        wasc=normalize_wasc(alert.get("wascid")),
                        tags=normalize_tags(alert.get("tags")),
                        url=url,
                        method=normalize_text(instance.get("method"), "GET").upper(),
                        param=normalize_text(instance.get("param")),
                        attack=normalize_text(instance.get("attack")),
                        evidence=normalize_text(instance.get("evidence")),
                        request_header=truncate_text(instance.get("request-header")),
                        request_body=truncate_text(instance.get("request-body")),
                        response_header=truncate_text(instance.get("response-header")),
                        response_body=truncate_text(instance.get("response-body")),
                        description=strip_html(alert.get("desc")),
                        solution=strip_html(alert.get("solution")),
                        reference=strip_html(alert.get("reference")),
                    )
                )
                next_index += 1
    return records


def slugify(value):
    slug = re.sub(r"[^A-Za-z0-9]+", "-", value or "").strip("-").lower()
    return slug or "alert"


def markdown_table_value(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def format_ai_output_for_triage_report(ai_output: str) -> str:
    ai_output = (ai_output or "").strip()
    fence_match = re.match(r"^```(?:markdown|md)\s*\n(?P<body>.*)\n```\s*$", ai_output, re.DOTALL | re.IGNORECASE)
    if fence_match:
        ai_output = fence_match.group("body").strip()

    formatted_lines = []
    in_code_block = False
    in_markdown_fence = False
    for line in ai_output.splitlines():
        stripped_line = line.lstrip()
        if re.match(r"^```(?:markdown|md)\s*$", stripped_line, re.IGNORECASE):
            in_markdown_fence = True
            continue
        if in_markdown_fence and stripped_line == "```":
            in_markdown_fence = False
            continue
        if stripped_line.startswith("```"):
            in_code_block = not in_code_block
            formatted_lines.append(line)
            continue
        if not in_code_block:
            heading_match = re.match(r"^(#{1,4})\s+(.+)$", line)
            if heading_match:
                formatted_lines.append(f"##### {heading_match.group(2)}")
                continue
        formatted_lines.append(line)
    return "\n".join(formatted_lines).strip()


def extract_ai_classification(ai_output: str) -> str:
    text = (ai_output or "").strip()
    if not text:
        return "Chưa có phân loại AI"

    labels = ("True Positive", "False Positive", "Needs Human Review")
    classification_pattern = "|".join(re.escape(label) for label in labels)
    heading_match = re.search(
        rf"phân loại(?:\s*\*\*)?\s*:?\s*(?:\n|\s)+(?:\*\*)?(?P<label>{classification_pattern})(?:\*\*)?",
        text,
        re.IGNORECASE,
    )
    if heading_match:
        matched_label = heading_match.group("label").lower()
        for label in labels:
            if label.lower() == matched_label:
                return label

    matches = []
    for label in labels:
        match = re.search(re.escape(label), text, re.IGNORECASE)
        if match:
            matches.append((match.start(), label))
    if matches:
        return sorted(matches, key=lambda item: item[0])[0][1]
    return "Chưa có phân loại AI"


def build_dynamic_triage_context(record):
    lines = [
        "Ngữ cảnh runtime cho triage động:",
        "- ZAP là DAST: phân loại dựa trên request/response runtime mà scanner quan sát được.",
        "- ZAP không chỉ ra dòng code. Không suy đoán root cause trong code nếu evidence HTTP chưa đủ.",
        "- True Positive: runtime evidence cho thấy cấu hình/hành vi lỗi tồn tại trên endpoint được quét.",
        "- False Positive: request/response cho thấy alert không áp dụng trong ngữ cảnh này hoặc là endpoint ngoài phạm vi.",
        "- Needs Human Review: evidence thiếu auth context, thiếu business impact, hoặc chỉ là informational signal.",
        "- Với alert Informational, chỉ nâng mức nghiêm trọng nếu response cho thấy dữ liệu nhạy cảm hoặc hành vi có thể khai thác.",
        "- Với endpoint localhost/lab, vẫn đánh giá theo hành vi quan sát được nhưng ghi rõ cần xác nhận môi trường deploy.",
    ]
    if record.attack != "N/A":
        lines.append("- Alert có attack payload; cần kiểm tra payload có làm thay đổi status code, header hoặc body theo hướng rủi ro không.")
    if record.evidence != "N/A":
        lines.append("- Evidence của ZAP phải được đối chiếu trực tiếp với response header/body trong report.")
    return "\n".join(lines)


def format_group_endpoints(group: ZapAlertGroup):
    lines = [
        "| # | Method | URL | Param | Evidence | Source JSON |",
        "|---|---|---|---|---|---|",
    ]
    for record in group.records:
        lines.append(
            "| {index} | {method} | `{url}` | `{param}` | `{evidence}` | `{source}` |".format(
                index=record.index,
                method=record.method,
                url=markdown_table_value(record.url),
                param=markdown_table_value(record.param),
                evidence=markdown_table_value(record.evidence),
                source=markdown_table_value(record.source_json),
            )
        )
    return "\n".join(lines)


def format_representative_runtime_evidence(group: ZapAlertGroup, limit=3):
    sections = []
    for record in group.records[:limit]:
        sections.extend(
            [
                f"### Endpoint {record.index}: {record.method} {record.url}",
                "",
                "Request:",
                "```http",
                record.request_header or f"{record.method} {record.url} HTTP/1.1",
                "```",
                "",
                "Request body:",
                "```text",
                record.request_body or "[Không có request body]",
                "```",
                "",
                "Response:",
                "```http",
                record.response_header or "[Không có response header trong JSON]",
                "```",
                "",
                "Response body excerpt:",
                "```text",
                record.response_body or "[Không có response body]",
                "```",
                "",
            ]
        )
    remaining = len(group.records) - limit
    if remaining > 0:
        sections.append(f"...[{remaining} endpoint còn lại được liệt kê trong bảng endpoint]")
    return "\n".join(sections).strip()


def build_group_prompt(group: ZapAlertGroup):
    record = group.records[0]
    sources = sorted({item.source_json for item in group.records})
    sites = sorted({item.site for item in group.records})
    return f"""Tôi dùng OWASP ZAP (DAST) để quét runtime của ứng dụng EShop và phát hiện một nhóm alert bảo mật cùng loại.
Bạn hãy đóng vai trò là chuyên gia bảo mật ứng dụng để triage alert này ở cấp nhóm, không lặp lại phân tích riêng cho từng endpoint nếu cùng root cause.
Hãy trả lời hoàn toàn bằng tiếng Việt, trừ các thuật ngữ chuẩn như True Positive, False Positive, Needs Human Review, CWE, WASC, OWASP, HTTP, header, payload.

Thông tin kỹ thuật:
- Mã alert: {group.alert_id}
- Alert name: {record.alert_name}
- Plugin ID: {record.plugin_id}
- Alert Ref: {record.alert_ref}
- Source JSON: {", ".join(sources)}
- Site: {", ".join(sites)}
- Số endpoint/request instance bị ảnh hưởng: {len(group.records)}
- Risk: {record.risk}
- Confidence: {record.confidence}
- CWE: {record.cwe}
- WASC: {record.wasc}
- Tags: {record.tags}

Danh sách endpoint bị ảnh hưởng:
{format_group_endpoints(group)}

Bằng chứng request/response runtime đại diện:
{format_representative_runtime_evidence(group)}

Mô tả ZAP:
{record.description or "N/A"}

Khuyến nghị ZAP:
{record.solution or "N/A"}

Tham khảo:
{record.reference or "N/A"}

{build_dynamic_triage_context(record)}

Hãy trả lời bằng Markdown với các mục:
1. Phân loại: True Positive / False Positive / Needs Human Review.
2. Lý do phân loại dựa trên runtime evidence của cả nhóm endpoint.
3. Tác động thực tế trong bối cảnh EShop.
4. Cách khắc phục cụ thể ở cấp cấu hình/root cause.
5. Ghi chú tester cần kiểm tra thêm nếu chưa đủ context.
"""


def build_prompt(record: ZapAlertRecord):
    return f"""Tôi dùng OWASP ZAP (DAST) để quét runtime của ứng dụng EShop và phát hiện một alert bảo mật.
Bạn hãy đóng vai trò là chuyên gia bảo mật ứng dụng để triage alert này.
Hãy trả lời hoàn toàn bằng tiếng Việt, trừ các thuật ngữ chuẩn như True Positive, False Positive, Needs Human Review, CWE, WASC, OWASP, HTTP, header, payload.

Thông tin kỹ thuật:
- Mã alert: {record.alert_id}
- Alert name: {record.alert_name}
- Plugin ID: {record.plugin_id}
- Alert Ref: {record.alert_ref}
- Source JSON: {record.source_json}
- Site: {record.site}
- URL: {record.url}
- Method: {record.method}
- Param: {record.param}
- Attack payload: {record.attack}
- Risk: {record.risk}
- Confidence: {record.confidence}
- CWE: {record.cwe}
- WASC: {record.wasc}
- Tags: {record.tags}
- Evidence: {record.evidence}

Request / bằng chứng request runtime:
```http
{record.request_header or "[Không có request header trong JSON]"}
```

Request body:
```text
{record.request_body or "[Không có request body]"}
```

Response / bằng chứng response runtime:
```http
{record.response_header or "[Không có response header trong JSON]"}
```

Response body excerpt:
```text
{record.response_body or "[Không có response body]"}
```

Mô tả ZAP:
{record.description or "N/A"}

Khuyến nghị ZAP:
{record.solution or "N/A"}

Tham khảo:
{record.reference or "N/A"}

{build_dynamic_triage_context(record)}

Hãy trả lời bằng Markdown với các mục:
1. Phân loại: True Positive / False Positive / Needs Human Review.
2. Lý do phân loại dựa trên runtime evidence.
3. Tác động thực tế trong bối cảnh EShop.
4. Cách khắc phục cụ thể.
5. Ghi chú tester cần kiểm tra thêm nếu chưa đủ context.
"""


def generate_ai_response(prompt, settings: AiSettings):
    if settings.provider == "openai-compatible":
        request_body = json.dumps(
            {
                "model": settings.model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": settings.max_tokens,
            }
        ).encode("utf-8")
        request = urllib.request.Request(
            f"{settings.base_url}/chat/completions",
            data=request_body,
            headers={
                "Authorization": f"Bearer {settings.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=90) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Lỗi OpenAI-compatible API ({exc.code}): {body}") from exc
        return payload["choices"][0]["message"]["content"]

    raise ValueError(f"Provider không được hỗ trợ: {settings.provider}")


def build_security_tag_lines(record: ZapAlertRecord):
    return [
        "| Thuộc tính | Giá trị |",
        "|---|---|",
        f"| Plugin ID | `{record.plugin_id}` |",
        f"| Alert Ref | `{record.alert_ref}` |",
        f"| Risk | `{record.risk}` |",
        f"| Confidence | `{record.confidence}` |",
        f"| CWE | {record.cwe} |",
        f"| WASC | {record.wasc} |",
        f"| Tags | {markdown_table_value(record.tags)} |",
        f"| Source JSON | `{record.source_json}` |",
    ]


def write_test_case_entries_report(records: List[ZapAlertRecord], output_dir, record_alert_ids=None):
    output_path = Path(output_dir)
    record_alert_ids = record_alert_ids or {}
    lines = [
        "# Danh sách test case kiểm chứng ZAP",
        "",
        "Tài liệu này tổng hợp test case kiểm chứng cho các alert ZAP theo từng request runtime. Mỗi entry trỏ về alert gốc trong `zap_triage_report.md`.",
    ]

    for record in records:
        request_line = f"{record.method} {record.url}"
        request_headers = record.request_header or f"{record.method} {record.url} HTTP/1.1"
        payload = record.request_body or "{}"
        lines.extend(
            [
                "",
                f"## TC-ZAP-{record.index:03d}",
                "",
                f"- Alert liên quan: {record_alert_ids.get(record.index, record.alert_id)}",
                f"- Mục tiêu test: Kiểm chứng alert `{record.alert_name}` bằng cách replay request runtime mà ZAP đã ghi nhận.",
                f"- Source JSON: `{record.source_json}`",
                "",
                "### Input",
                "",
                "```http",
                request_line,
                "```",
                "",
                "Headers:",
                "```http",
                request_headers,
                "```",
                "",
                "Payload:",
                "```json",
                payload,
                "```",
                "",
                "### Thao tác",
                "",
                "1. Đảm bảo backend/frontend EShop và ngữ cảnh auth tương ứng đang chạy.",
                "2. Chuẩn bị token, cookie hoặc session nếu request của ZAP có header xác thực.",
                "3. Replay request theo method, URL, headers từ ZAP.",
                "4. Ghi nhận status code, response headers và response body.",
                "5. So sánh kết quả mới với evidence ZAP trong triage report.",
                "",
                "### Kết quả cần ghi nhận",
                "",
                f"- Nếu còn lỗi: Response vẫn chứa evidence `{record.evidence}` hoặc hành vi runtime vẫn khớp alert `{record.alert_name}`.",
                "- Nếu đã an toàn: Response không còn evidence liên quan hoặc server trả trạng thái chặn/hardening phù hợp.",
                "",
                "### Trạng thái",
                "",
                "Chưa kiểm chứng",
            ]
        )

    lines.extend(
        [
            "",
            "## Ghi chú sử dụng",
            "",
            "- `Alert liên quan` trỏ về ID alert trong `zap_triage_report.md`.",
            "- ZAP có thể ghi nhận endpoint ngoài phạm vi nếu browser hoặc môi trường runtime gọi domain khác; dùng `--target-prefix` để lọc target chính.",
            "- Với endpoint yêu cầu đăng nhập, tester cần tái tạo auth context trước khi replay request.",
            "- Kết luận cuối cùng vẫn phân loại theo `True Positive`, `False Positive`, hoặc `Needs Human Review`.",
            "",
        ]
    )

    report_path = output_path / "zap_test_cases.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def build_security_tag_lines_for_group(group: ZapAlertGroup):
    record = group.records[0]
    sources = sorted({item.source_json for item in group.records})
    sites = sorted({item.site for item in group.records})
    return [
        "| Thuộc tính | Giá trị |",
        "|---|---|",
        f"| Plugin ID | `{record.plugin_id}` |",
        f"| Alert Ref | `{record.alert_ref}` |",
        f"| Risk | `{record.risk}` |",
        f"| Confidence | `{record.confidence}` |",
        f"| CWE | {record.cwe} |",
        f"| WASC | {record.wasc} |",
        f"| Tags | {markdown_table_value(record.tags)} |",
        f"| Source JSON | {', '.join(f'`{source}`' for source in sources)} |",
        f"| Site | {', '.join(f'`{site}`' for site in sites)} |",
    ]


def build_group_endpoint_table_lines(group: ZapAlertGroup):
    lines = [
        "| # | Method | URL | Param | Evidence |",
        "|---|---|---|---|---|",
    ]
    for record in group.records:
        lines.append(
            "| {index} | {method} | `{url}` | `{param}` | `{evidence}` |".format(
                index=record.index,
                method=record.method,
                url=markdown_table_value(record.url),
                param=markdown_table_value(record.param),
                evidence=markdown_table_value(record.evidence),
            )
        )
    return lines


def write_triage_outputs(records: List[ZapAlertRecord], ai_outputs: Dict[int, str], output_dir):
    output_path = Path(output_dir)
    alerts_dir = output_path / "alerts"
    alerts_dir.mkdir(parents=True, exist_ok=True)
    groups = group_alert_records(records)
    record_alert_ids = {
        record.index: group.alert_id
        for group in groups
        for record in group.records
    }

    table_lines = [
        "| # | Alert | Endpoints | Risk | Confidence | CWE | WASC | Phân loại AI | Kết quả AI | Trạng thái kiểm chứng thủ công |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    detail_sections = []

    for group in groups:
        record = group.records[0]
        slug = f"{group.index:03d}_{slugify(record.alert_name)}"
        prompt_path = alerts_dir / f"{slug}_prompt.md"
        ai_output_path = alerts_dir / f"{slug}_ai_output.md"
        prompt_path.write_text(build_group_prompt(group), encoding="utf-8")
        ai_output = ai_outputs.get(group.index, "").strip()
        formatted_ai_output = format_ai_output_for_triage_report(ai_output)
        ai_classification = extract_ai_classification(ai_output)
        ai_output_path.write_text(ai_output, encoding="utf-8")

        table_lines.append(
            "| {index} | `{alert}` | {endpoints} | {risk} | {confidence} | {cwe} | {wasc} | {classification} | `{ai}` | Chưa kiểm chứng |".format(
                index=group.index,
                alert=markdown_table_value(record.alert_name),
                endpoints=len(group.records),
                risk=markdown_table_value(record.risk),
                confidence=markdown_table_value(record.confidence),
                cwe=markdown_table_value(record.cwe),
                wasc=markdown_table_value(record.wasc),
                classification=markdown_table_value(ai_classification),
                ai=ai_output_path.relative_to(output_path),
            )
        )
        detail_sections.extend(
            [
                f"### {group.alert_id}: {record.alert_name}",
                "",
                "#### Tags lỗi",
                *build_security_tag_lines_for_group(group),
                "",
                "#### Thông tin alert nhóm",
                f"- Số endpoint/request instance bị ảnh hưởng: {len(group.records)}",
                f"- Phân loại AI: {ai_classification}",
                "- Trạng thái kiểm chứng thủ công: Chưa kiểm chứng",
                "",
                "#### Endpoints bị ảnh hưởng",
                *build_group_endpoint_table_lines(group),
                "",
                "#### Bằng chứng runtime đại diện",
                "",
                "Request:",
                "```http",
                record.request_header or f"{record.method} {record.url} HTTP/1.1",
                "```",
                "",
                "Request body:",
                "```text",
                record.request_body or "[Không có request body]",
                "```",
                "",
                "Response:",
                "```http",
                record.response_header or "[Không có response header trong JSON]",
                "```",
                "",
                "Response body excerpt:",
                "```text",
                record.response_body or "[Không có response body]",
                "```",
                "",
                "#### Phân tích AI",
                formatted_ai_output or "Chưa có output AI cho alert này.",
                "",
            ]
        )

    sources = sorted({record.source_json for record in records})
    sites = sorted({record.site for record in records})
    report = "\n".join(
        [
            "# Báo cáo ZAP AI Triage",
            "",
            "## Tổng quan",
            "",
            f"- Tổng số alert instance trong input: {len(records)}",
            f"- Tổng số alert sau khi gom nhóm: {len(groups)}",
            f"- Source JSON: {', '.join(f'`{source}`' for source in sources) if sources else 'N/A'}",
            f"- Scan target/site: {', '.join(f'`{site}`' for site in sites) if sites else 'N/A'}",
            "- Script đọc `site[].alerts[].instances[]` từ JSON ZAP, không hardcode số lượng alert.",
            "- ZAP là DAST nên evidence chính là request/response runtime, không phải dòng code.",
            "- Phân loại của AI là hỗ trợ triage; kết luận cuối cùng vẫn cần tester kiểm chứng.",
            "",
            "## Bảng tổng hợp alerts",
            "",
            *table_lines,
            "",
            "## Chi tiết từng alert",
            "",
            *detail_sections,
            "## Checklist kiểm chứng thủ công",
            "",
            "- Xác nhận URL có thuộc target scan cần báo cáo hay không.",
            "- Replay request với cùng method, headers, payload và auth context.",
            "- Đối chiếu evidence trong response mới với evidence mà ZAP đã ghi nhận.",
            "- Kiểm tra các alert trùng root cause để gom lại khi viết báo cáo cuối.",
            "- Chỉ chốt `True Positive`, `False Positive`, hoặc `Needs Human Review` sau khi có đủ runtime context.",
            "",
        ]
    )

    report_path = output_path / "zap_triage_report.md"
    report_path.write_text(report, encoding="utf-8")
    write_test_case_entries_report(records, output_path, record_alert_ids)
    return report_path


def read_json_file(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def collect_records_from_files(paths, target_prefixes=None, limit=None):
    records = []
    next_index = 1
    for path in paths:
        data = read_json_file(path)
        file_records = collect_alert_records(
            data,
            Path(path).name,
            start_index=next_index,
            target_prefixes=target_prefixes,
        )
        records.extend(file_records)
        next_index += len(file_records)
        if limit is not None and len(records) >= limit:
            return records[:limit]
    return records


def alert_group_key(record: ZapAlertRecord):
    return (
        record.plugin_id,
        record.alert_ref,
        record.alert_name,
        record.risk,
        record.confidence,
        record.cwe,
        record.wasc,
        record.tags,
    )


def group_alert_records(records: List[ZapAlertRecord]):
    groups_by_key = {}
    groups = []
    for record in records:
        key = alert_group_key(record)
        if key not in groups_by_key:
            group = ZapAlertGroup(
                index=len(groups) + 1,
                alert_id=f"ZAP-{len(groups) + 1:03d}",
                records=[],
            )
            groups_by_key[key] = group
            groups.append(group)
        groups_by_key[key].records.append(record)
    return groups


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Run AI triage for OWASP ZAP JSON alerts.")
    parser.add_argument("json_files", nargs="+", help="Một hoặc nhiều file JSON report của ZAP.")
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Thư mục output cho zap_triage_report.md, zap_test_cases.md và alerts/*.",
    )
    parser.add_argument(
        "--target-prefix",
        action="append",
        default=[],
        help="Chỉ lấy URL bắt đầu bằng prefix này. Có thể truyền nhiều lần, ví dụ --target-prefix http://localhost:3000.",
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Không gọi AI provider; chỉ sinh prompt, skeleton AI output và markdown testcase.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Giới hạn số alert instance cần xử lý.",
    )
    return parser.parse_args(argv)


def main(argv=None):
    configure_console_encoding()
    args = parse_args(sys.argv[1:] if argv is None else argv)

    if args.limit is not None and args.limit <= 0:
        print("--limit phải là số nguyên dương.")
        return 1

    try:
        records = collect_records_from_files(
            args.json_files,
            target_prefixes=args.target_prefix,
            limit=args.limit,
        )
    except Exception as exc:
        print(f"Lỗi khi đọc JSON ZAP: {exc}")
        return 1

    if not records:
        print("Không tìm thấy alert instance nào trong input ZAP.")
        return 0

    groups = group_alert_records(records)
    print(f"Tìm thấy {len(records)} alert instances từ ZAP.")
    print(f"Gom thành {len(groups)} alert groups để AI triage.")
    settings = None
    if not args.offline:
        try:
            settings = get_ai_settings()
        except ValueError as exc:
            print(f"Lỗi cấu hình AI: {exc}")
            print("Có thể chạy --offline để sinh prompt/report trước khi có API key.")
            return 1
        print(f"Provider: {settings.provider} | Model: {settings.model}")

    ai_outputs = {}
    for group in groups:
        record = group.records[0]
        prompt = build_group_prompt(group)
        print(f"Triaging {group.alert_id}: {record.alert_name} ({len(group.records)} endpoint)")
        if args.offline:
            ai_outputs[group.index] = (
                "## Output AI\n\n"
                "Chưa gọi AI provider. Prompt đã được lưu để reviewer chạy triage sau.\n\n"
                "## Kiểm chứng thủ công\n\n"
                "- Trạng thái: Needs Human Review\n"
            )
            continue
        try:
            ai_outputs[group.index] = generate_ai_response(prompt, settings)
        except Exception as exc:
            print(
                f"Lỗi khi gọi AI provider cho {group.alert_id} "
                f"({record.alert_name}, {len(group.records)} endpoint): {exc}"
            )
            print("Dừng triage để tránh sinh report không có phân tích AI đầy đủ.")
            return 1

    report_path = write_triage_outputs(records, ai_outputs, args.output_dir)
    print(f"Đã tạo ZAP triage report: {report_path}")
    return 0


if __name__ == "__main__":
    configure_console_encoding()
    sys.exit(main())
