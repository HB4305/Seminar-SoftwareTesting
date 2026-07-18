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


class AiSettings(NamedTuple):
    provider: str
    model: str
    api_key: str
    base_url: Optional[str] = None


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

    return AiSettings(provider=provider, model=model, api_key=api_key, base_url=base_url)


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

Hãy trả lời bằng Markdown với các mục:
1. True Positive / False Positive / Needs Manual Verification.
2. Giải thích lỗ hổng trong bối cảnh EShop.
3. PoC hoặc testcase kiểm chứng.
4. Impact thực tế.
5. Remediation cụ thể.
6. Human validation cần làm trước khi kết luận cuối cùng.
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


def write_triage_outputs(records: List[FindingRecord], ai_outputs: Dict[int, str], output_dir):
    output_path = Path(output_dir)
    findings_dir = output_path / "findings"
    findings_dir.mkdir(parents=True, exist_ok=True)

    table_lines = [
        "| # | Rule | File | Line | Severity | CWE | OWASP | Likelihood | Impact | Confidence | AI Output | Human Validation |",
        "|---|---|---|---:|---|---|---|---|---|---|---|---|",
    ]

    for record in records:
        slug = f"{record.index:03d}_{slugify(record.rule_id)}"
        prompt_path = findings_dir / f"{slug}_prompt.md"
        ai_output_path = findings_dir / f"{slug}_ai_output.md"
        prompt_path.write_text(build_prompt(record), encoding="utf-8")
        ai_output_path.write_text(ai_outputs.get(record.index, ""), encoding="utf-8")
        table_lines.append(
            "| {index} | `{rule}` | `{file}` | {line} | {severity} | {cwe} | {owasp} | {likelihood} | {impact} | {confidence} | `{ai}` | Needs Manual Verification |".format(
                index=record.index,
                rule=record.rule_id,
                file=record.file_path,
                line=record.line,
                severity=record.severity,
                cwe=record.cwe,
                owasp=record.owasp,
                likelihood=record.likelihood,
                impact=record.impact,
                confidence=record.confidence,
                ai=ai_output_path.relative_to(output_path),
            )
        )

    report = "\n".join(
        [
            "# Semgrep AI Triage Report",
            "",
            "## Summary",
            "",
            f"- Total findings in input: {len(records)}",
            "- The script iterates over every item in `results`; this number is not hardcoded.",
            "- Status values are draft outputs. Final conclusion requires human validation.",
            "",
            "## Findings",
            "",
            *table_lines,
            "",
            "## Human Validation Checklist",
            "",
            "- Confirm whether duplicate findings share one root cause.",
            "- Reproduce exploitable behavior with a PoC or runtime request when possible.",
            "- Mark each finding as `Confirmed`, `False Positive`, `Needs Manual Verification`, or `Environment Noise` before submission.",
            "- Link screenshots, logs, Semgrep JSON, and ZAP evidence in the combined report.",
            "",
        ]
    )
    report_path = output_path / "semgrep_triage_report.md"
    report_path.write_text(report, encoding="utf-8")
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
    sys.exit(main())
