import argparse
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
NO_REQUEST_BODY = "Không có request body."


def configure_console_encoding(stdout=None, stderr=None):
    """Prefer UTF-8 output on Windows consoles that support reconfigure()."""
    for stream in (stdout or sys.stdout, stderr or sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            try:
                reconfigure(encoding="utf-8")
            except Exception:
                pass


class AiSettings(NamedTuple):
    provider: str
    model: str
    api_key: str
    base_url: Optional[str] = None
    max_tokens: int = DEFAULT_AI_MAX_TOKENS


class FindingRecord(NamedTuple):
    index: int
    rule_id: str
    file_path: str
    line: int
    severity: str
    message: str
    code: str
    cwe: str
    owasp: str
    likelihood: str
    impact: str
    confidence: str


class RuntimeMapping(NamedTuple):
    title: str
    affected_feature: str
    method: str
    url: str
    headers: str
    payload: str
    pre_test_setup: str
    test_objective: str
    vulnerable_behavior: str
    secure_behavior: str
    zap_related_alert: str
    difference: str
    conclusion: str
    confidence: str
    note: str


def load_env_file(env_file):
    """Read a simple KEY=VALUE .env file without mutating os.environ."""
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
    """Prefer project/runtime .env, then src/semgrep/.env."""
    candidates = [
        Path.cwd() / ".env",
        SCRIPT_DIR / ".env",
        SCRIPT_DIR / ".env.example",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def get_ai_settings(env: Optional[Mapping[str, str]] = None, env_file=None):
    merged_env = {}
    default_env_file = find_default_env_file() if env_file is None else env_file
    merged_env.update(load_env_file(default_env_file))
    merged_env.update(dict(os.environ if env is None else env))

    provider = merged_env.get("AI_PROVIDER", "gemini").strip().lower()
    default_model = "gemini-2.5-flash" if provider == "gemini" else ""
    model = merged_env.get("AI_MODEL", default_model).strip()
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

    if provider == "gemini":
        api_key = merged_env.get("AI_API_KEY") or merged_env.get("GEMINI_API_KEY")
        base_url = None
    elif provider in {"openai-compatible", "openai"}:
        provider = "openai-compatible"
        api_key = (
            merged_env.get("AI_API_KEY")
            or merged_env.get("OPENROUTER_API_KEY")
            or merged_env.get("OPENAI_API_KEY")
        )
        base_url = (
            merged_env.get("OPENROUTER_BASE_URL")
            or merged_env.get("OPENAI_BASE_URL")
            or ""
        ).rstrip("/")
    else:
        raise ValueError("AI_PROVIDER chỉ hỗ trợ 'gemini' hoặc 'openai-compatible'.")

    if not model:
        raise ValueError("Chưa thiết lập AI_MODEL cho provider đã chọn.")
    if not api_key:
        if provider == "gemini":
            raise ValueError("Chưa thiết lập AI_API_KEY hoặc GEMINI_API_KEY.")
        raise ValueError("Chưa thiết lập AI_API_KEY, OPENROUTER_API_KEY hoặc OPENAI_API_KEY.")
    if provider == "openai-compatible" and not base_url:
        raise ValueError("Chưa thiết lập OPENROUTER_BASE_URL hoặc OPENAI_BASE_URL cho provider openai-compatible.")

    return AiSettings(
        provider=provider,
        model=model,
        api_key=api_key,
        base_url=base_url,
        max_tokens=max_tokens,
    )


def resolve_file_path(original_path, source_root=None):
    """
    Resolve absolute, repo-relative, or scan-result paths to a local source file.
    """
    if not original_path:
        return None

    path = Path(original_path)
    if path.exists():
        return path

    normalized = original_path.replace("\\", "/")
    if source_root:
        candidate = Path(source_root) / normalized
        if candidate.exists():
            return candidate

    parts = normalized.split("/")
    subpath = None
    if "eshop-sut" in parts:
        idx = parts.index("eshop-sut")
        subpath = Path(*parts[idx:])
    elif "backend" in parts:
        idx = parts.index("backend")
        subpath = Path("eshop-sut", *parts[idx:])
    elif "frontend-mobile" in parts:
        idx = parts.index("frontend-mobile")
        subpath = Path("eshop-sut", *parts[idx:])

    candidates = []
    if subpath:
        candidates.extend(
            [
                Path.cwd() / ".." / "eshop-sut" / Path(*subpath.parts[1:]),
                Path.cwd() / ".." / "EShop" / subpath,
                SCRIPT_DIR / ".." / ".." / ".." / "eshop-sut" / Path(*subpath.parts[1:]),
                SCRIPT_DIR / ".." / ".." / ".." / "EShop" / subpath,
            ]
        )
    if source_root:
        candidates.append(Path(source_root) / normalized)

    for candidate in candidates:
        candidate = candidate.resolve()
        if candidate.exists():
            return candidate

    filename = Path(normalized).name
    parent_dir = SCRIPT_DIR.parents[2]
    for root, _dirs, files in os.walk(parent_dir):
        if filename in files:
            full_path = Path(root) / filename
            full_path_text = str(full_path)
            if "eshop-sut" in full_path_text or "EShop" in full_path_text:
                return full_path

    return None


def get_source_code_snippet(file_path, line_number, context_lines=5):
    if not file_path or not Path(file_path).exists() or not line_number:
        return ""
    try:
        lines = Path(file_path).read_text(encoding="utf-8", errors="ignore").splitlines()
    except Exception as exc:
        return f"[Không đọc được file nguồn: {exc}]"

    start_idx = max(0, line_number - context_lines - 1)
    end_idx = min(len(lines), line_number + context_lines)
    snippet_lines = []
    for idx in range(start_idx, end_idx):
        line_num = idx + 1
        marker = "=> " if line_num == line_number else "   "
        separator = ": " if lines[idx] else ":"
        snippet_lines.append(f"{marker}{line_num}{separator}{lines[idx]}")
    return "\n".join(snippet_lines)


def join_metadata(value):
    if isinstance(value, list):
        return ", ".join(str(item) for item in value)
    if value:
        return str(value)
    return "N/A"


def infer_file_role(file_path):
    normalized = str(file_path or "").replace("\\", "/").lower()
    name = Path(normalized).name
    if (
        name.startswith("test_")
        or name.endswith(".test.js")
        or name.endswith(".spec.js")
        or "/test/" in normalized
        or "/tests/" in normalized
    ):
        return "mã test/helper"
    if "/backend/" in normalized and name in {"server.js", "app.js", "index.js"}:
        return "entrypoint runtime backend"
    if "/frontend-" in normalized or "/frontend/" in normalized:
        return "mã runtime của ứng dụng"
    if "/backend/" in normalized:
        return "mã backend của ứng dụng"
    return "chưa rõ; reviewer cần xác nhận file này có được deploy hay không"


def build_static_triage_context(record):
    file_role = infer_file_role(record.file_path)
    code_lower = (record.code or "").lower()
    rule_lower = (record.rule_id or "").lower()
    context_lines = [
        "Ngữ cảnh source cho triage tĩnh:",
        "- Đọc và đối chiếu source evidence trước khi phân loại.",
        "- Semgrep là SAST: phân loại dựa trên bằng chứng source code và ngữ cảnh deploy, không dựa trên HTTP response.",
        "- EShop đang được quét như ứng dụng lab local; finding liên quan localhost cần kiểm tra môi trường trước khi kết luận rủi ro cuối.",
        f"- Vai trò file: {file_role}.",
        "- True Positive: source evidence khớp rule và code lỗi reachable trong runtime/ngữ cảnh ứng dụng liên quan.",
        "- False Positive: source evidence hoặc vai trò file chứng minh finding không phải lỗ hổng thật của ứng dụng.",
        "- Needs Human Review: chưa rõ config, deploy usage, runtime reachability hoặc độ nhạy cảm dữ liệu.",
        "- Nếu đây là mã test/helper, không phân loại là True Positive trừ khi file được deploy hoặc được runtime code dùng lại.",
        "- HTTP localhost có thể chỉ dùng cho dev/lab; chỉ phân loại False Positive khi source/config chứng minh production không bị ảnh hưởng.",
        "- Nếu nhiều finding cùng một root cause, hãy nêu trong phần giải thích nhưng vẫn chọn một trong ba phân loại.",
    ]
    if "localhost" in code_lower or "http://127.0.0.1" in code_lower:
        context_lines.append(
            "- Snippet này tham chiếu endpoint HTTP local; cần kiểm tra production API_URL/base URL trước khi xem là lỗ hổng truyền tải thật."
        )
    if "jwt" in rule_lower or "secret" in code_lower:
        context_lines.append(
            "- Với finding JWT/secret, cần xác nhận secret có ký/xác minh token thật của ứng dụng hay không và file có thuộc runtime code hay không."
        )
    return "\n".join(context_lines)


def collect_finding_records(findings: Iterable[dict], source_root=None):
    records = []
    for index, finding in enumerate(findings, start=1):
        extra = finding.get("extra", {})
        metadata = extra.get("metadata", {})
        line = finding.get("start", {}).get("line") or 0
        code = extra.get("lines", "")
        rule_id = finding.get("check_id", "unknown-rule")
        message = extra.get("message", "")

        if not code or code == "requires login":
            resolved_path = resolve_file_path(finding.get("path", ""), source_root=source_root)
            is_http_finding = (
                "insecure-request" in rule_id.lower()
                or "cleartext" in message.lower()
            )
            context_lines = 15 if is_http_finding else 5
            code = (
                get_source_code_snippet(resolved_path, line, context_lines=context_lines)
                if resolved_path
                else ""
            )
            if not code:
                code = "[Không có source snippet trong JSON và không định vị được file nguồn]"

        records.append(
            FindingRecord(
                index=index,
                rule_id=rule_id,
                file_path=finding.get("path", "unknown-file"),
                line=line,
                severity=extra.get("severity", "UNKNOWN"),
                message=message,
                code=code,
                cwe=join_metadata(metadata.get("cwe")),
                owasp=join_metadata(metadata.get("owasp")),
                likelihood=metadata.get("likelihood", "N/A"),
                impact=metadata.get("impact", "N/A"),
                confidence=metadata.get("confidence", "N/A"),
            )
        )
    return records


def build_prompt(record):
    return f"""Tôi dùng công cụ Semgrep (SAST) để quét mã nguồn và phát hiện một finding bảo mật.
Bạn hãy đóng vai trò là chuyên gia bảo mật ứng dụng để triage finding này.
Hãy trả lời hoàn toàn bằng tiếng Việt, trừ các thuật ngữ chuẩn như True Positive, False Positive, Needs Human Review, CWE, OWASP.

Thông tin kỹ thuật:
- Mã finding: SEMGREP-{record.index:03d}
- Rule ID: {record.rule_id}
- File nguồn: {record.file_path}
- Dòng: {record.line}
- Severity: {record.severity}
- CWE: {record.cwe}
- OWASP: {record.owasp}
- Likelihood: {record.likelihood}
- Impact: {record.impact}
- Confidence: {record.confidence}
- Cảnh báo Semgrep: {record.message}

Source code context / bằng chứng mã nguồn:
```text
{record.code}
```

{build_static_triage_context(record)}

Hãy trả lời bằng Markdown với các mục:
1. Phân loại: True Positive / False Positive / Needs Human Review.
2. Lý do phân loại dựa trên source evidence.
3. Tác động thực tế trong bối cảnh EShop.
4. Cách khắc phục cụ thể.
5. Ghi chú cần tester kiểm tra thêm nếu chưa đủ context.
"""


def generate_ai_response(prompt, settings):
    if settings.provider == "gemini":
        try:
            from google import genai
        except ImportError as exc:
            raise RuntimeError("Vui lòng cài đặt thư viện: pip install google-genai") from exc

        client = genai.Client(api_key=settings.api_key)
        response = client.models.generate_content(model=settings.model, contents=prompt)
        return response.text

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


def slugify(value):
    slug = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return slug or "finding"


def extract_first_http_url(text):
    match = re.search(r"http://[^\s'\"),;]+", text or "")
    return match.group(0) if match else ""


def extract_runtime_url_from_code(text):
    marked_line = re.search(r"(?m)^=>\s*\d+:\s*(?P<code>.*)$", text or "")
    candidates = [marked_line.group("code")] if marked_line else []
    candidates.append(text or "")

    for candidate in candidates:
        explicit_url = extract_first_http_url(candidate)
        if explicit_url:
            return explicit_url

        api_url_match = re.search(r"\$\{API_URL\}([^`'\"),;]+)", candidate)
        if api_url_match:
            return f"http://localhost:3000/api{api_url_match.group(1)}"

    return ""


def infer_method_from_code(code):
    lowered = (code or "").lower()
    method_match = re.search(r"\bmethod\s*:\s*['\"]([A-Za-z]+)['\"]", code or "")
    if method_match:
        return method_match.group(1).upper()
    for method in ("post", "put", "patch", "delete", "get"):
        if re.search(rf"\b{method}\s*\(", lowered) or f".{method}(" in lowered:
            return method.upper()
    return "GET"


def extract_json_stringify_object(code):
    source = code or ""
    marked_line = re.search(r"(?m)^=>\s*\d+:", source)
    if marked_line:
        source = source[marked_line.start() :]
    normalized = re.sub(r"(?m)^(?:=>\s*|\s*)\d+:\s?", "", source)
    match = re.search(r"\bbody\s*:\s*JSON\.stringify\s*\(", normalized)
    if not match:
        return ""

    start = normalized.find("{", match.end())
    if start < 0:
        return ""

    depth = 0
    quote = None
    escaped = False
    for index in range(start, len(normalized)):
        char = normalized[index]
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            continue
        if char in {'"', "'", "`"}:
            quote = char
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return normalized[start : index + 1]
    return ""


def split_top_level_properties(object_text):
    if not object_text.startswith("{") or not object_text.endswith("}"):
        return []

    properties = []
    current = []
    depths = {"{": 0, "[": 0, "(": 0}
    closing = {"}": "{", "]": "[", ")": "("}
    quote = None
    escaped = False

    for char in object_text[1:-1]:
        if quote:
            current.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            continue
        if char in {'"', "'", "`"}:
            quote = char
            current.append(char)
        elif char in depths:
            depths[char] += 1
            current.append(char)
        elif char in closing:
            depths[closing[char]] = max(0, depths[closing[char]] - 1)
            current.append(char)
        elif char == "," and not any(depths.values()):
            if "".join(current).strip():
                properties.append("".join(current).strip())
            current = []
        else:
            current.append(char)

    if "".join(current).strip():
        properties.append("".join(current).strip())
    return properties


def extract_payload_fields(code):
    object_text = extract_json_stringify_object(code)
    fields = []
    for prop in split_top_level_properties(object_text):
        match = re.match(
            r"\s*(?:['\"](?P<quoted>[^'\"]+)['\"]|(?P<plain>[A-Za-z_$][\w$]*))\s*(?::(?P<value>.*))?$",
            prop,
            re.DOTALL,
        )
        if match:
            fields.append(
                (
                    match.group("quoted") or match.group("plain"),
                    (match.group("value") or "").strip(),
                )
            )
    return fields


def sample_payload_value(field, expression, url):
    samples = {
        "email": "{{test_email}}",
        "password": "{{test_password}}",
        "name": "{{test_name}}",
        "phone": "{{test_phone}}",
        "shippingAddress": "{{shipping_address}}",
        "resetToken": "{{reset_token}}",
        "newPassword": "{{new_password}}",
        "code": "{{coupon_code}}",
        "total_amount": 100000,
        "user_id": "{{user_id}}",
        "items": [
            {
                "product_id": "{{product_id}}",
                "quantity": 1,
                "price": 100000,
            }
        ],
        "coupon_id": "{{coupon_id}}",
    }
    if field == "coupon_id" and url.rstrip("/").endswith("/checkout"):
        return None
    if field in samples:
        return samples[field]
    variable = re.sub(r"(?<!^)(?=[A-Z])", "_", field).lower()
    return "{{" + variable + "}}"


def infer_sample_payload(code, method, url):
    if method.upper() in {"GET", "HEAD"}:
        return NO_REQUEST_BODY

    fields = extract_payload_fields(code)
    if not fields:
        return "{}"
    payload = {
        field: sample_payload_value(field, expression, url)
        for field, expression in fields
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def runtime_mapping_for_record(record):
    rule = record.rule_id.lower()
    if "jwt-hardcode" in rule or "hardcoded-jwt-secret" in rule:
        return RuntimeMapping(
            title="JWT Secret hardcode",
            affected_feature="Xác thực JWT / phân quyền admin",
            method="GET",
            url="http://localhost:3000/api/users/me",
            headers="Authorization: Bearer <forged_admin_jwt>\nContent-Type: application/json",
            payload=NO_REQUEST_BODY,
            pre_test_setup=(
                "1. Dùng `src/semgrep/exploit.js` để tạo JWT giả.\n"
                "2. Copy token sinh ra vào header Authorization.\n"
                "3. Đảm bảo backend EShop đang chạy tại port 3000."
            ),
            test_objective="Kiểm tra backend có chấp nhận JWT giả được ký bằng hardcoded secret hay không.",
            vulnerable_behavior="Server trả `200 OK` và chấp nhận token giả.",
            secure_behavior="Server trả `401 Unauthorized` hoặc `403 Forbidden`.",
            zap_related_alert="ZAP không phát hiện trực tiếp; điểm yếu xác thực có thể cần authenticated active scan.",
            difference=(
                "- Semgrep phát hiện root cause trong source code.\n"
                "- ZAP cần runtime request hợp lệ hoặc attack path để quan sát hành vi."
            ),
            conclusion="Semgrep phù hợp phát hiện secret hardcode; Postman dùng để xác nhận runtime exploitability.",
            confidence="Medium",
            note="Endpoint được suy luận từ cách backend verify JWT, cần xác nhận khi test.",
        )

    if "insecure-request" in rule or "cleartext" in record.message.lower():
        url = extract_runtime_url_from_code(record.code) or "http://localhost:3000/<api-path>"
        method = infer_method_from_code(record.code)
        return RuntimeMapping(
            title="HTTP request không mã hóa",
            affected_feature="Bảo mật truyền tải frontend/API",
            method=method,
            url=url,
            headers="Content-Type: application/json",
            payload=infer_sample_payload(record.code, method, url),
            pre_test_setup=(
                "1. Mở source line được Semgrep báo để xác nhận API path.\n"
                "2. Đảm bảo backend/frontend local đang chạy.\n"
                "3. Gửi request bằng Postman và ghi nhận URL đang dùng HTTP."
            ),
            test_objective="Kiểm tra request đang dùng HTTP cleartext thay vì HTTPS.",
            vulnerable_behavior="Request gọi thành công qua `http://` hoặc dữ liệu nhạy cảm đi qua kênh không mã hóa.",
            secure_behavior="Ứng dụng dùng `https://` hoặc cấu hình base URL an toàn theo môi trường.",
            zap_related_alert="Có thể xuất hiện như evidence truyền tải runtime nếu ZAP quan sát được request tương ứng.",
            difference=(
                "- Semgrep phát hiện hardcoded `http://` trong source code.\n"
                "- ZAP chỉ thấy lỗi nếu request đó thực sự được crawl/spider hoặc gửi qua proxy."
            ),
            conclusion="Semgrep giúp tìm đường dẫn HTTP trong code; Postman/ZAP xác nhận hành vi runtime.",
            confidence="High" if url != "http://localhost:3000/<api-path>" else "Low",
            note="Endpoint được trích từ source snippet nếu có; nếu thiếu path cần reviewer map thủ công.",
        )

    return RuntimeMapping(
        title=record.message.strip(".") or "Semgrep Finding",
        affected_feature="Cần mapping thủ công từ source sang runtime",
        method="GET",
        url="http://localhost:3000/<map-endpoint>",
        headers="Content-Type: application/json",
        payload=NO_REQUEST_BODY,
        pre_test_setup=(
            "1. Đọc source evidence để xác định endpoint hoặc feature liên quan.\n"
            "2. Điền method, URL, header và payload thật trước khi test Postman."
        ),
        test_objective="Xác thực finding Semgrep bằng hành vi runtime nếu có thể.",
        vulnerable_behavior="Hành vi lỗi tái hiện được trong Postman.",
        secure_behavior="Hành vi lỗi không còn tái hiện hoặc được chặn an toàn.",
        zap_related_alert="Chưa xác định cho đến khi đối chiếu với ZAP report.",
        difference=(
            "- Semgrep cung cấp source evidence.\n"
            "- ZAP cung cấp runtime HTTP evidence nếu scan đi qua endpoint tương ứng."
        ),
        conclusion="Cần human validation để kết luận khả năng khai thác runtime.",
        confidence="Low",
        note="Semgrep finding này chưa có mapping rule tự động.",
    )


def write_test_case_entries_report(records: List[FindingRecord], output_dir):
    output_path = Path(output_dir)
    lines = [
        "# Danh sách test case kiểm chứng Semgrep",
        "",
        "Tài liệu này tổng hợp test case kiểm chứng cho các finding Semgrep theo từng entry riêng. Mỗi entry có liên kết về finding gốc để reviewer biết test case đang xác minh cảnh báo nào.",
    ]

    for record in records:
        mapping = runtime_mapping_for_record(record)
        request = f"{mapping.method} {mapping.url}"
        action = "Gửi request và ghi nhận status code, response body."
        if mapping.payload == NO_REQUEST_BODY:
            payload_lines = [
                "Payload:",
                NO_REQUEST_BODY,
                "",
                "- Nguồn payload: Suy luận từ HTTP method không sử dụng request body.",
                "- Độ tin cậy payload: High",
            ]
        elif mapping.payload == "{}":
            payload_lines = [
                "Payload mẫu:",
                "```json",
                mapping.payload,
                "```",
                "",
                "- Nguồn payload: Không trích xuất được request body từ source context.",
                "- Độ tin cậy payload: Low",
                "- Tester cần điền payload thật trước khi chạy PoC.",
            ]
        else:
            payload_lines = [
                "Payload mẫu:",
                "```json",
                mapping.payload,
                "```",
                "",
                "- Nguồn payload: Tự động suy luận từ `body: JSON.stringify(...)` trong source.",
                "- Độ tin cậy payload: High",
                "- Thay các biến `{{...}}` bằng giá trị Postman environment trước khi chạy PoC.",
            ]
        lines.extend(
            [
                "",
                f"## TC-SEMGREP-{record.index:03d}",
                "",
                f"- Finding liên quan: SEMGREP-{record.index:03d}",
                f"- Mục tiêu test: {mapping.test_objective}",
                "",
                "### Input",
                "",
                "```http",
                request,
                "```",
                "",
                "Headers:",
                "```http",
                mapping.headers,
                "```",
                "",
                *payload_lines,
                "",
                "### Thao tác",
                "",
                mapping.pre_test_setup,
                "",
                action,
                "",
                "### Kết quả cần ghi nhận",
                "",
                f"- Nếu còn lỗi: {mapping.vulnerable_behavior}",
                f"- Nếu đã an toàn: {mapping.secure_behavior}",
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
            "- `Finding liên quan` trỏ về ID finding trong `semgrep_triage_report.md`.",
            "- Với finding chưa map được endpoint thật, tester cần đọc source evidence rồi điền lại URL/header/payload trước khi kiểm chứng.",
            "- Kết quả cuối cùng vẫn phân loại theo `True Positive`, `False Positive`, hoặc `Needs Human Review`.",
            "",
        ]
    )

    report_path = output_path / "semgrep_test_cases.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def build_triage_postman_lines(record: FindingRecord) -> List[str]:
    mapping = runtime_mapping_for_record(record)
    if mapping.payload == NO_REQUEST_BODY:
        payload_lines = [
            "Payload:",
            NO_REQUEST_BODY,
            "",
            "- Nguồn payload: Suy luận từ HTTP method không sử dụng request body.",
            "- Độ tin cậy payload: High",
        ]
    elif mapping.payload == "{}":
        payload_lines = [
            "Payload mẫu:",
            "```json",
            mapping.payload,
            "```",
            "",
            "- Nguồn payload: Không trích xuất được request body từ source context.",
            "- Độ tin cậy payload: Low",
            "- Tester cần điền payload thật trước khi chạy PoC.",
        ]
    else:
        payload_lines = [
            "Payload mẫu:",
            "```json",
            mapping.payload,
            "```",
            "",
            "- Nguồn payload: Tự động suy luận từ `body: JSON.stringify(...)` trong source.",
            "- Độ tin cậy payload: High",
            "- Thay các biến `{{...}}` bằng giá trị Postman environment trước khi chạy PoC.",
        ]

    return [
        "#### Postman/PoC tự động",
        f"- Mục tiêu test: {mapping.test_objective}",
        f"- Feature ảnh hưởng: {mapping.affected_feature}",
        f"- Method: `{mapping.method}`",
        f"- URL: `{mapping.url}`",
        f"- Độ tin cậy mapping: {mapping.confidence}",
        f"- Ghi chú mapping: {mapping.note}",
        "",
        "Headers:",
        "```http",
        mapping.headers,
        "```",
        "",
        *payload_lines,
        "",
        "Pre-test setup:",
        "```text",
        mapping.pre_test_setup,
        "```",
        "",
        "Kết quả kỳ vọng:",
        f"- Nếu còn lỗi: {mapping.vulnerable_behavior}",
        f"- Nếu đã an toàn: {mapping.secure_behavior}",
        "",
    ]


def build_security_tag_lines(record: FindingRecord) -> List[str]:
    return [
        "| Thuộc tính | Giá trị |",
        "|---|---|",
        f"| Rule ID | `{record.rule_id}` |",
        f"| Severity | `{record.severity}` |",
        f"| CWE | {record.cwe} |",
        f"| OWASP | {record.owasp} |",
        f"| Likelihood | `{record.likelihood}` |",
        f"| Impact | `{record.impact}` |",
        f"| Confidence | `{record.confidence}` |",
    ]


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


def write_triage_outputs(records: List[FindingRecord], ai_outputs: Dict[int, str], output_dir):
    output_path = Path(output_dir)
    findings_dir = output_path / "findings"
    findings_dir.mkdir(parents=True, exist_ok=True)

    table_lines = [
        "| # | Quy tắc | Tệp | Dòng | Mức độ | CWE | OWASP | Kết quả AI | Trạng thái kiểm chứng |",
        "|---|---|---|---:|---|---|---|---|---|",
    ]
    detail_sections = []

    for record in records:
        slug = f"{record.index:03d}_{slugify(record.rule_id)}"
        prompt_path = findings_dir / f"{slug}_prompt.md"
        ai_output_path = findings_dir / f"{slug}_ai_output.md"
        prompt_path.write_text(build_prompt(record), encoding="utf-8")
        ai_output = ai_outputs.get(record.index, "").strip()
        formatted_ai_output = format_ai_output_for_triage_report(ai_output)
        ai_output_path.write_text(ai_output, encoding="utf-8")
        table_lines.append(
            "| {index} | `{rule}` | `{file}` | {line} | {severity} | {cwe} | {owasp} | `{ai}` | Cần người kiểm chứng |".format(
                index=record.index,
                rule=record.rule_id,
                file=record.file_path,
                line=record.line,
                severity=record.severity,
                cwe=record.cwe,
                owasp=record.owasp,
                ai=ai_output_path.relative_to(output_path),
            )
        )
        detail_sections.extend(
            [
                f"### SEMGREP-{record.index:03d}: {record.rule_id}",
                "",
                "#### Tags lỗi",
                *build_security_tag_lines(record),
                "",
                "#### Thông tin finding",
                f"- File: `{record.file_path}`",
                f"- Dòng: {record.line}",
                f"- Trạng thái kiểm chứng: Needs Human Review",
                "",
                "#### Bằng chứng mã nguồn",
                "```text",
                record.code,
                "```",
                "",
                *build_triage_postman_lines(record),
                "#### Phân tích AI",
                formatted_ai_output or "Chưa có output AI cho finding này.",
                "",
            ]
        )

    report = "\n".join(
        [
            "# Báo cáo Semgrep AI Triage",
            "",
            "## Tổng quan",
            "",
            f"- Tổng số finding trong input: {len(records)}",
            "- Script đọc toàn bộ mảng `results` từ JSON Semgrep, không hardcode số lượng finding.",
            "- Phân loại của AI là hỗ trợ triage; kết luận cuối cùng vẫn cần tester kiểm chứng.",
            "",
            "## Bảng tổng hợp findings",
            "",
            *table_lines,
            "",
            "## Chi tiết từng finding",
            "",
            *detail_sections,
            "## Checklist kiểm chứng thủ công",
            "",
            "- Xác nhận finding có nằm trong code được chạy/deploy thật hay không.",
            "- Kiểm tra các finding trùng root cause để gom lại khi viết báo cáo cuối.",
            "- Reproduce bằng PoC hoặc runtime request nếu finding phụ thuộc hành vi chạy thật.",
            "- Chỉ chốt `True Positive`, `False Positive`, hoặc `Needs Human Review` sau khi có đủ context.",
            "- Gắn source evidence, log, screenshot hoặc ZAP/Postman evidence nếu có.",
            "",
        ]
    )
    report_path = output_path / "semgrep_triage_report.md"
    report_path.write_text(report, encoding="utf-8")
    write_test_case_entries_report(records, output_path)
    return report_path


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Run AI triage for Semgrep JSON results.")
    parser.add_argument("json_file", help="Semgrep JSON result file, for example src/semgrep/sg_rs.json")
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Output directory for semgrep_triage_report.md and per-finding files.",
    )
    parser.add_argument(
        "--source-root",
        default=None,
        help="Optional root of the scanned source tree for fallback source snippets.",
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Do not call AI provider; generate prompts, skeleton AI outputs, and summary report.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional maximum number of findings to triage.",
    )
    return parser.parse_args(argv)


def main(argv=None):
    configure_console_encoding()
    args = parse_args(sys.argv[1:] if argv is None else argv)

    try:
        data = json.loads(Path(args.json_file).read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"Lỗi khi đọc file {args.json_file}: {exc}")
        return 1

    findings = data.get("results", [])
    if args.limit is not None:
        findings = findings[: args.limit]
    if not findings:
        print("Không tìm thấy finding bảo mật nào trong file JSON.")
        return 0

    records = collect_finding_records(findings, source_root=args.source_root)
    print(f"Tìm thấy {len(records)} findings từ Semgrep.")

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
    for record in records:
        prompt = build_prompt(record)
        print(f"Triaging #{record.index}: {record.rule_id} tại {record.file_path}:{record.line}")
        if args.offline:
            ai_outputs[record.index] = (
                "## Output AI\n\n"
                "Chưa gọi AI provider. Prompt đã được lưu để reviewer chạy triage sau.\n\n"
                "## Kiểm chứng thủ công\n\n"
                "- Trạng thái: Needs Human Review\n"
            )
            continue
        try:
            ai_outputs[record.index] = generate_ai_response(prompt, settings)
        except Exception as exc:
            print(
                f"Lỗi khi gọi AI provider cho finding #{record.index} "
                f"({record.rule_id} tại {record.file_path}:{record.line}): {exc}"
            )
            print("Dừng triage để tránh sinh report không có phân tích AI đầy đủ.")
            return 1

    report_path = write_triage_outputs(records, ai_outputs, args.output_dir)
    print(f"Đã tạo Semgrep triage report: {report_path}")
    return 0


if __name__ == "__main__":
    configure_console_encoding()
    sys.exit(main())
