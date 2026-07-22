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
        snippet_lines.append(f"{marker}{line_num}: {lines[idx]}")
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
        return "test/helper code"
    if "/backend/" in normalized and name in {"server.js", "app.js", "index.js"}:
        return "backend runtime entrypoint"
    if "/frontend-" in normalized or "/frontend/" in normalized:
        return "application runtime code"
    if "/backend/" in normalized:
        return "backend application code"
    return "unknown; reviewer must confirm whether this file is deployed"


def build_static_triage_context(record):
    file_role = infer_file_role(record.file_path)
    code_lower = (record.code or "").lower()
    rule_lower = (record.rule_id or "").lower()
    context_lines = [
        "Project/source context for static triage:",
        "- Read and compare the source evidence before classification.",
        "- Semgrep is SAST: classify from source evidence and deployment context, not from HTTP responses.",
        "- EShop is scanned as a local lab app; localhost findings need environment review before final risk.",
        f"- File role: {file_role}.",
        "- True Positive: source evidence matches the rule and the vulnerable code is reachable in the relevant app/runtime context.",
        "- False Positive: source evidence or file role proves the finding is not a real vulnerability for this app.",
        "- Needs Human Review: config, deployment usage, runtime reachability, or data sensitivity is unknown.",
        "- If this is test/helper code, do not classify it as True Positive unless it is deployed or reused by runtime code.",
        "- localhost HTTP can be dev/lab-only; classify it as False Positive only when source/config proves production is not affected.",
        "- If several findings share one root cause, mention that in the explanation but still choose one of the three classifications.",
    ]
    if "localhost" in code_lower or "http://127.0.0.1" in code_lower:
        context_lines.append(
            "- This snippet references a local HTTP endpoint; verify production API_URL/base URL before calling it a real transport-security vulnerability."
        )
    if "jwt" in rule_lower or "secret" in code_lower:
        context_lines.append(
            "- For JWT/secret findings, confirm whether the secret signs or verifies real application tokens and whether the file is part of runtime code."
        )
    return "\n".join(context_lines)


def collect_finding_records(findings: Iterable[dict], source_root=None):
    records = []
    for index, finding in enumerate(findings, start=1):
        extra = finding.get("extra", {})
        metadata = extra.get("metadata", {})
        line = finding.get("start", {}).get("line") or 0
        code = extra.get("lines", "")

        if not code or code == "requires login":
            resolved_path = resolve_file_path(finding.get("path", ""), source_root=source_root)
            code = get_source_code_snippet(resolved_path, line) if resolved_path else ""
            if not code:
                code = "[Không có source snippet trong JSON và không định vị được file nguồn]"

        records.append(
            FindingRecord(
                index=index,
                rule_id=finding.get("check_id", "unknown-rule"),
                file_path=finding.get("path", "unknown-file"),
                line=line,
                severity=extra.get("severity", "UNKNOWN"),
                message=extra.get("message", ""),
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

Thông tin kỹ thuật:
- Finding index: {record.index}
- Rule ID: {record.rule_id}
- File: {record.file_path}
- Dòng: {record.line}
- Severity: {record.severity}
- CWE: {record.cwe}
- OWASP: {record.owasp}
- Likelihood: {record.likelihood}
- Impact: {record.impact}
- Confidence: {record.confidence}
- Cảnh báo Semgrep: {record.message}

Source code context:
```text
{record.code}
```

{build_static_triage_context(record)}

Hãy trả lời bằng Markdown với các mục:
1. Classification: True Positive / False Positive / Needs Human Review.
2. Giải thích lỗ hổng trong bối cảnh EShop.
3. PoC hoặc testcase kiểm chứng.
4. Impact thực tế.
5. Remediation cụ thể.
6. Human validation cần làm trước khi kết luận cuối cùng, nhất là file có chạy thật không và production config có bị ảnh hưởng không.
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


def infer_method_from_code(code):
    lowered = (code or "").lower()
    for method in ("post", "put", "patch", "delete", "get"):
        if re.search(rf"\b{method}\s*\(", lowered) or f".{method}(" in lowered:
            return method.upper()
    return "GET"


def runtime_mapping_for_record(record):
    rule = record.rule_id.lower()
    if "jwt-hardcode" in rule or "hardcoded-jwt-secret" in rule:
        return RuntimeMapping(
            title="Hardcoded JWT Secret",
            affected_feature="JWT authentication / admin authorization",
            method="GET",
            url="http://localhost:3000/api/users/me",
            headers="Authorization: Bearer <forged_admin_jwt>\nContent-Type: application/json",
            payload="{}",
            pre_test_setup=(
                "1. Dùng `src/semgrep/exploit.js` để tạo JWT giả.\n"
                "2. Copy token sinh ra vào header Authorization.\n"
                "3. Đảm bảo backend EShop đang chạy tại port 3000."
            ),
            test_objective="Kiểm tra backend có chấp nhận JWT giả được ký bằng hardcoded secret hay không.",
            vulnerable_behavior="Server trả `200 OK` và chấp nhận token giả.",
            secure_behavior="Server trả `401 Unauthorized` hoặc `403 Forbidden`.",
            zap_related_alert="Not directly detected / Authentication weakness may require authenticated active scan.",
            difference=(
                "- Semgrep phát hiện root cause trong source code.\n"
                "- ZAP cần runtime request hợp lệ hoặc attack path để quan sát hành vi."
            ),
            conclusion="Semgrep phù hợp phát hiện secret hardcode; Postman dùng để xác nhận runtime exploitability.",
            confidence="Medium",
            note="Endpoint được suy luận từ cách backend verify JWT, cần xác nhận khi test.",
        )

    if "insecure-request" in rule or "cleartext" in record.message.lower():
        url = extract_first_http_url(record.code) or "http://localhost:3000/<api-path>"
        method = infer_method_from_code(record.code)
        return RuntimeMapping(
            title="Insecure HTTP Request",
            affected_feature="Frontend/API transport security",
            method=method,
            url=url,
            headers="Content-Type: application/json",
            payload="{}",
            pre_test_setup=(
                "1. Mở source line được Semgrep báo để xác nhận API path.\n"
                "2. Đảm bảo backend/frontend local đang chạy.\n"
                "3. Gửi request bằng Postman và ghi nhận URL đang dùng HTTP."
            ),
            test_objective="Kiểm tra request đang dùng HTTP cleartext thay vì HTTPS.",
            vulnerable_behavior="Request gọi thành công qua `http://` hoặc dữ liệu nhạy cảm đi qua kênh không mã hóa.",
            secure_behavior="Ứng dụng dùng `https://` hoặc cấu hình base URL an toàn theo môi trường.",
            zap_related_alert="May appear as passive/runtime transport or mixed-content evidence if ZAP observes the same request.",
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
        affected_feature="Needs manual source-to-runtime mapping",
        method="GET",
        url="http://localhost:3000/<map-endpoint>",
        headers="Content-Type: application/json",
        payload="{}",
        pre_test_setup=(
            "1. Đọc source evidence để xác định endpoint hoặc feature liên quan.\n"
            "2. Điền method, URL, header và payload thật trước khi test Postman."
        ),
        test_objective="Xác thực finding Semgrep bằng hành vi runtime nếu có thể.",
        vulnerable_behavior="Hành vi lỗi tái hiện được trong Postman.",
        secure_behavior="Hành vi lỗi không còn tái hiện hoặc được chặn an toàn.",
        zap_related_alert="Unknown until mapped against ZAP report.",
        difference=(
            "- Semgrep cung cấp source evidence.\n"
            "- ZAP cung cấp runtime HTTP evidence nếu scan đi qua endpoint tương ứng."
        ),
        conclusion="Cần human validation để kết luận khả năng khai thác runtime.",
        confidence="Low",
        note="Semgrep finding này chưa có mapping rule tự động.",
    )


def write_postman_validation_report(records: List[FindingRecord], output_dir):
    output_path = Path(output_dir)
    lines = [
        "# Semgrep Postman Validation Report",
        "",
        "Report này format finding Semgrep theo kiểu gần với ZAP Alert và thêm test case để reviewer copy sang Postman.",
        "",
        "## Comparison Matrix",
        "",
        "| Semgrep Finding | Source Evidence | Postman Result | ZAP Related Alert | Conclusion |",
        "|---|---|---|---|---|",
    ]

    mappings = []
    for record in records:
        mapping = runtime_mapping_for_record(record)
        mappings.append((record, mapping))
        lines.append(
            f"| SEMGREP-{record.index:03d}: {mapping.title} | `{record.file_path}:{record.line}` | Needs Manual Verification | {mapping.zap_related_alert} | {mapping.conclusion} |"
        )

    for record, mapping in mappings:
        lines.extend(
            [
                "",
                f"## SEMGREP-{record.index:03d}: {mapping.title}",
                "",
                "### 1. Alert Summary",
                f"- Tool: Semgrep",
                f"- Type: SAST",
                f"- Rule ID: `{record.rule_id}`",
                f"- Severity: {record.severity}",
                f"- CWE: {record.cwe}",
                f"- OWASP: {record.owasp}",
                "- Status: Needs Manual Verification",
                "",
                "### 2. Source Evidence",
                f"- File: `{record.file_path}`",
                f"- Line: {record.line}",
                "- Vulnerable code:",
                "```text",
                record.code,
                "```",
                "",
                "### 3. Runtime Mapping",
                f"- Affected feature: {mapping.affected_feature}",
                f"- Related endpoint: `{mapping.method} {mapping.url}`",
                f"- Method: `{mapping.method}`",
                "- Base URL: `http://localhost:3000`",
                "- Auth required: Yes" if "Authorization:" in mapping.headers else "- Auth required: No / depends on endpoint",
                f"- Mapping confidence: {mapping.confidence}",
                f"- Mapping note: {mapping.note}",
                "",
                "### 4. Postman Test Case",
                f"- Test objective: {mapping.test_objective}",
                "- URL:",
                "```http",
                f"{mapping.method} {mapping.url}",
                "```",
                "- Headers:",
                "```http",
                mapping.headers,
                "```",
                "- Payload:",
                "```json",
                mapping.payload,
                "```",
                "- Pre-test setup:",
                "```text",
                mapping.pre_test_setup,
                "```",
                "",
                "### 5. Expected Result",
                f"- Vulnerable behavior: {mapping.vulnerable_behavior}",
                f"- Secure behavior: {mapping.secure_behavior}",
                "- Evidence to capture: status code, response body, screenshot Postman, request URL/header/body.",
                "",
                "### 6. ZAP Comparison",
                f"- ZAP related alert: {mapping.zap_related_alert}",
                "- Difference:",
                mapping.difference,
                f"- Conclusion: {mapping.conclusion}",
            ]
        )

    report_path = output_path / "semgrep_postman_validation_report.md"
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report_path


def write_triage_outputs(records: List[FindingRecord], ai_outputs: Dict[int, str], output_dir):
    output_path = Path(output_dir)
    findings_dir = output_path / "findings"
    findings_dir.mkdir(parents=True, exist_ok=True)

    table_lines = [
        "| # | Rule | File | Line | Severity | CWE | OWASP | AI Output | Trạng thái kiểm chứng |",
        "|---|---|---|---:|---|---|---|---|---|",
    ]
    detail_sections = []

    for record in records:
        slug = f"{record.index:03d}_{slugify(record.rule_id)}"
        prompt_path = findings_dir / f"{slug}_prompt.md"
        ai_output_path = findings_dir / f"{slug}_ai_output.md"
        prompt_path.write_text(build_prompt(record), encoding="utf-8")
        ai_output = ai_outputs.get(record.index, "").strip()
        ai_output_path.write_text(ai_output, encoding="utf-8")
        table_lines.append(
            "| {index} | `{rule}` | `{file}` | {line} | {severity} | {cwe} | {owasp} | `{ai}` | Needs Human Review |".format(
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
                "#### Thông tin finding",
                f"- File: `{record.file_path}`",
                f"- Dòng: {record.line}",
                f"- Severity: {record.severity}",
                f"- CWE: {record.cwe}",
                f"- OWASP: {record.owasp}",
                f"- Likelihood / Impact / Confidence: {record.likelihood} / {record.impact} / {record.confidence}",
                f"- Trạng thái kiểm chứng: Needs Human Review",
                "",
                "#### Source evidence",
                "```text",
                record.code,
                "```",
                "",
                "#### Phân tích AI",
                ai_output or "Chưa có output AI cho finding này.",
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
    write_postman_validation_report(records, output_path)
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
                "## AI Output\n\n"
                "Chưa gọi AI provider. Prompt đã được lưu để reviewer chạy triage sau.\n\n"
                "## Human Validation\n\n"
                "- Status: Needs Manual Verification\n"
            )
            continue
        try:
            ai_outputs[record.index] = generate_ai_response(prompt, settings)
        except Exception as exc:
            ai_outputs[record.index] = (
                "## AI Output Error\n\n"
                f"Không gọi được AI provider cho finding này: {exc}\n\n"
                "## Human Validation\n\n"
                "- Status: Needs Manual Verification\n"
            )

    report_path = write_triage_outputs(records, ai_outputs, args.output_dir)
    print(f"Đã tạo Semgrep triage report: {report_path}")
    return 0


if __name__ == "__main__":
    configure_console_encoding()
    sys.exit(main())
