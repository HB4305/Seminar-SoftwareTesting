import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT_PATH = Path(__file__).with_name("semgrep_ai_triage.py")


def load_triage_module():
    spec = importlib.util.spec_from_file_location("src_semgrep_ai_triage", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SemgrepAiTriageWorkflowTest(unittest.TestCase):
    def test_module_loads_without_google_genai_installed(self):
        triage = load_triage_module()

        self.assertTrue(hasattr(triage, "load_env_file"))

    def test_collect_finding_records_keeps_all_findings_and_metadata(self):
        triage = load_triage_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            source_root = Path(tmpdir)
            source_file = source_root / "backend" / "server.js"
            source_file.parent.mkdir(parents=True)
            source_file.write_text(
                "\n".join(
                    [
                        "const express = require('express');",
                        "const SECRET_KEY = 'secret';",
                        "jwt.sign(payload, SECRET_KEY);",
                    ]
                ),
                encoding="utf-8",
            )
            findings = [
                {
                    "check_id": "rule.one",
                    "path": "backend/server.js",
                    "start": {"line": 2},
                    "extra": {
                        "severity": "WARNING",
                        "message": "Hard-coded credential",
                        "lines": "requires login",
                        "metadata": {
                            "cwe": ["CWE-798"],
                            "owasp": ["A07:2025"],
                            "likelihood": "HIGH",
                            "impact": "MEDIUM",
                            "confidence": "HIGH",
                        },
                    },
                },
                {
                    "check_id": "rule.two",
                    "path": "frontend-mobile/App.js",
                    "start": {"line": 10},
                    "extra": {
                        "severity": "ERROR",
                        "message": "Cleartext request",
                        "lines": "fetch('http://localhost:3000')",
                        "metadata": {},
                    },
                },
            ]

            records = triage.collect_finding_records(findings, source_root=source_root)

        self.assertEqual(len(records), 2)
        self.assertEqual(records[0].rule_id, "rule.one")
        self.assertEqual(records[0].cwe, "CWE-798")
        self.assertEqual(records[0].owasp, "A07:2025")
        self.assertIn("SECRET_KEY", records[0].code)
        self.assertEqual(records[1].severity, "ERROR")

    def test_get_ai_settings_supports_openrouter_variables(self):
        triage = load_triage_module()

        settings = triage.get_ai_settings(
            {
                "AI_PROVIDER": "openai-compatible",
                "AI_MODEL": "google/gemini-2.5-flash-lite",
                "OPENROUTER_API_KEY": "openrouter-key",
                "OPENROUTER_BASE_URL": "https://openrouter.ai/api/v1",
            },
            env_file="",
        )

        self.assertEqual(settings.provider, "openai-compatible")
        self.assertEqual(settings.model, "google/gemini-2.5-flash-lite")
        self.assertEqual(settings.api_key, "openrouter-key")
        self.assertEqual(settings.base_url, "https://openrouter.ai/api/v1")

    def test_get_ai_settings_reads_max_tokens_for_openrouter(self):
        triage = load_triage_module()

        settings = triage.get_ai_settings(
            {
                "AI_PROVIDER": "openai-compatible",
                "AI_MODEL": "google/gemini-2.5-flash-lite",
                "OPENROUTER_API_KEY": "openrouter-key",
                "OPENROUTER_BASE_URL": "https://openrouter.ai/api/v1",
                "AI_MAX_TOKENS": "1200",
            },
            env_file="",
        )

        self.assertEqual(settings.max_tokens, 1200)

    def test_openai_compatible_request_limits_max_tokens(self):
        triage = load_triage_module()
        settings = triage.AiSettings(
            provider="openai-compatible",
            model="google/gemini-2.5-flash-lite",
            api_key="openrouter-key",
            base_url="https://openrouter.ai/api/v1",
        )
        captured = {}
        response = mock.Mock()
        response.__enter__ = mock.Mock(return_value=response)
        response.__exit__ = mock.Mock(return_value=None)
        response.read = mock.Mock(
            return_value=b'{"choices":[{"message":{"content":"triage ok"}}]}'
        )

        def fake_urlopen(request, timeout):
            captured["body"] = json.loads(request.data.decode("utf-8"))
            captured["timeout"] = timeout
            return response

        with mock.patch("urllib.request.urlopen", side_effect=fake_urlopen):
            result = triage.generate_ai_response("prompt", settings)

        self.assertEqual(result, "triage ok")
        self.assertEqual(captured["body"]["max_tokens"], 1800)
        self.assertEqual(captured["timeout"], 90)

    def test_configure_console_encoding_reconfigures_utf8_capable_streams(self):
        triage = load_triage_module()

        class FakeStream:
            def __init__(self):
                self.encoding = "cp1252"
                self.requested_encoding = None

            def reconfigure(self, encoding):
                self.requested_encoding = encoding

        stdout = FakeStream()
        stderr = FakeStream()

        triage.configure_console_encoding(stdout, stderr)

        self.assertEqual(stdout.requested_encoding, "utf-8")
        self.assertEqual(stderr.requested_encoding, "utf-8")

    def test_write_triage_outputs_creates_summary_and_per_finding_files(self):
        triage = load_triage_module()
        record = triage.FindingRecord(
            index=1,
            rule_id="rule.one",
            file_path="backend/server.js",
            line=2,
            severity="WARNING",
            message="Hard-coded credential",
            code="const SECRET_KEY = 'secret';",
            cwe="CWE-798",
            owasp="A07:2025",
            likelihood="HIGH",
            impact="MEDIUM",
            confidence="HIGH",
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)

            report_path = triage.write_triage_outputs(
                [record],
                {1: "AI output body"},
                output_dir,
            )

            report = report_path.read_text(encoding="utf-8")
            prompt = (output_dir / "findings" / "001_rule-one_prompt.md").read_text(
                encoding="utf-8"
            )
            ai_output = (
                output_dir / "findings" / "001_rule-one_ai_output.md"
            ).read_text(encoding="utf-8")

        self.assertIn("semgrep_triage_report", report_path.name)
        self.assertIn("rule.one", report)
        self.assertIn(
            "| # | Quy tắc | Tệp | Dòng | Mức độ | CWE | OWASP | Kết quả AI | Trạng thái kiểm chứng |",
            report,
        )
        self.assertNotIn("| # | Rule | File | Dòng | Severity | CWE | OWASP | Output AI |", report)
        self.assertIn("| 1 | `rule.one` | `backend/server.js` | 2 | WARNING | CWE-798 | A07:2025 |", report)
        self.assertIn("Cần người kiểm chứng", report)
        self.assertNotIn("| Needs Human Review |", report)
        self.assertIn("## Chi tiết từng finding", report)
        self.assertIn("### SEMGREP-001: rule.one", report)
        self.assertIn("### Phân tích AI", report)
        self.assertIn("AI output body", report)
        self.assertIn("Trạng thái kiểm chứng", report)
        self.assertIn("const SECRET_KEY", prompt)
        self.assertIn("AI output body", ai_output)

    def test_build_prompt_includes_source_first_three_state_classification_context(self):
        triage = load_triage_module()
        record = triage.FindingRecord(
            index=4,
            rule_id="typescript.react.security.react-insecure-request.react-insecure-request",
            file_path="eshop-sut/frontend-mobile/App.js",
            line=174,
            severity="ERROR",
            message="Unencrypted request over HTTP detected.",
            code='const API_URL = "http://localhost:3000";',
            cwe="CWE-319",
            owasp="A02:2021",
            likelihood="LOW",
            impact="MEDIUM",
            confidence="MEDIUM",
        )

        prompt = triage.build_prompt(record)

        self.assertIn("Hãy trả lời hoàn toàn bằng tiếng Việt", prompt)
        self.assertIn("Ngữ cảnh source cho triage tĩnh", prompt)
        self.assertIn("Đọc và đối chiếu source evidence trước khi phân loại", prompt)
        self.assertIn("Vai trò file: mã runtime của ứng dụng", prompt)
        self.assertIn("HTTP localhost có thể chỉ dùng cho dev/lab", prompt)
        self.assertIn("Phân loại: True Positive / False Positive / Needs Human Review", prompt)
        self.assertIn("Lý do phân loại dựa trên source evidence", prompt)
        self.assertIn("Ghi chú cần tester kiểm tra thêm nếu chưa đủ context", prompt)
        self.assertNotIn("PoC hoặc testcase kiểm chứng", prompt)
        self.assertNotIn("Duplicate / Same Root Cause", prompt)

    def test_build_prompt_marks_test_files_as_test_helper_context(self):
        triage = load_triage_module()
        record = triage.FindingRecord(
            index=3,
            rule_id="javascript.jsonwebtoken.security.jwt-hardcode.hardcoded-jwt-secret",
            file_path="eshop-sut/backend/test_profile.js",
            line=4,
            severity="WARNING",
            message="Hard-coded credential",
            code='jwt.sign({ id: 2 }, "secret");',
            cwe="CWE-798",
            owasp="A07:2021",
            likelihood="HIGH",
            impact="MEDIUM",
            confidence="HIGH",
        )

        prompt = triage.build_prompt(record)

        self.assertIn("Vai trò file: mã test/helper", prompt)
        self.assertIn("không phân loại là True Positive trừ khi file được deploy", prompt)

    def test_write_triage_outputs_creates_test_case_entries_report(self):
        triage = load_triage_module()
        records = [
            triage.FindingRecord(
                index=1,
                rule_id="javascript.jsonwebtoken.security.jwt-hardcode.hardcoded-jwt-secret",
                file_path="backend/server.js",
                line=51,
                severity="WARNING",
                message="Hard-coded credential",
                code='const SECRET_KEY = "super_secret_key_that_should_not_be_here";',
                cwe="CWE-798: Use of Hard-coded Credentials",
                owasp="A07:2021 - Identification and Authentication Failures",
                likelihood="HIGH",
                impact="MEDIUM",
                confidence="HIGH",
            ),
            triage.FindingRecord(
                index=2,
                rule_id="typescript.react.security.react-insecure-request.react-insecure-request",
                file_path="frontend-mobile/App.js",
                line=174,
                severity="ERROR",
                message="Unencrypted request over HTTP detected.",
                code='await axios.get("http://localhost:3000/api/products");',
                cwe="CWE-319: Cleartext Transmission of Sensitive Information",
                owasp="A02:2021 - Cryptographic Failures",
                likelihood="LOW",
                impact="MEDIUM",
                confidence="MEDIUM",
            ),
        ]
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)

            triage.write_triage_outputs(records, {}, output_dir)

            report = (output_dir / "semgrep_test_cases.md").read_text(
                encoding="utf-8"
            )
            old_report_exists = (output_dir / "semgrep_postman_validation_report.md").exists()
            old_table_report_exists = (output_dir / "semgrep_test_case_table.md").exists()

        self.assertFalse(old_report_exists)
        self.assertFalse(old_table_report_exists)
        self.assertIn("# Danh sách test case kiểm chứng Semgrep", report)
        self.assertIn("theo từng entry riêng", report)
        self.assertIn("## TC-SEMGREP-001", report)
        self.assertIn("- Finding liên quan: SEMGREP-001", report)
        self.assertIn("### Input", report)
        self.assertIn("### Thao tác", report)
        self.assertIn("### Kết quả cần ghi nhận", report)
        self.assertNotIn("### Expected output", report)
        self.assertNotIn("### Actual output", report)
        self.assertIn("### Trạng thái", report)
        self.assertNotIn("| Mã test case | Finding liên quan |", report)
        self.assertIn("GET http://localhost:3000/api/users/me", report)
        self.assertIn("Authorization: Bearer <forged_admin_jwt>", report)
        self.assertIn("Gửi request và ghi nhận status code, response body", report)
        self.assertIn("## TC-SEMGREP-002", report)
        self.assertIn("- Finding liên quan: SEMGREP-002", report)
        self.assertIn("GET http://localhost:3000/api/products", report)
        self.assertIn("Chưa kiểm chứng", report)
        self.assertNotIn("Độ tin cậy mapping", report)
        self.assertNotIn("Bằng chứng cần thu thập", report)

    def test_triage_report_detail_entries_include_security_tags(self):
        triage = load_triage_module()
        record = triage.FindingRecord(
            index=1,
            rule_id="javascript.jsonwebtoken.security.jwt-hardcode.hardcoded-jwt-secret",
            file_path="backend/server.js",
            line=51,
            severity="WARNING",
            message="Hard-coded credential",
            code='const SECRET_KEY = "super_secret_key_that_should_not_be_here";',
            cwe="CWE-798: Use of Hard-coded Credentials",
            owasp="A07:2021 - Identification and Authentication Failures",
            likelihood="HIGH",
            impact="MEDIUM",
            confidence="HIGH",
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)

            triage.write_triage_outputs({record.index: record}.values(), {}, output_dir)

            report = (output_dir / "semgrep_triage_report.md").read_text(
                encoding="utf-8"
            )

        self.assertIn("### SEMGREP-001:", report)
        self.assertIn("#### Tags lỗi", report)
        self.assertIn("| Thuộc tính | Giá trị |", report)
        self.assertIn("|---|---|", report)
        self.assertIn(
            "| Rule ID | `javascript.jsonwebtoken.security.jwt-hardcode.hardcoded-jwt-secret` |",
            report,
        )
        self.assertIn("| Severity | `WARNING` |", report)
        self.assertIn("| CWE | CWE-798: Use of Hard-coded Credentials |", report)
        self.assertIn(
            "| OWASP | A07:2021 - Identification and Authentication Failures |",
            report,
        )
        self.assertIn("| Likelihood | `HIGH` |", report)
        self.assertIn("| Impact | `MEDIUM` |", report)
        self.assertIn("| Confidence | `HIGH` |", report)

        finding_info = report.split("#### Thông tin finding", 1)[1].split(
            "#### Bằng chứng mã nguồn", 1
        )[0]
        self.assertIn("- File: `backend/server.js`", finding_info)
        self.assertIn("- Dòng: 51", finding_info)
        self.assertIn("- Trạng thái kiểm chứng: Needs Human Review", finding_info)
        self.assertNotIn("- Severity:", finding_info)
        self.assertNotIn("- CWE:", finding_info)
        self.assertNotIn("- OWASP:", finding_info)
        self.assertNotIn("Likelihood / Impact / Confidence", finding_info)

    def test_triage_report_demotes_ai_headings_inside_finding_details(self):
        triage = load_triage_module()
        record = triage.FindingRecord(
            index=1,
            rule_id="rule.one",
            file_path="backend/server.js",
            line=2,
            severity="WARNING",
            message="Hard-coded credential",
            code="const SECRET_KEY = 'secret';",
            cwe="CWE-798",
            owasp="A07:2025",
            likelihood="HIGH",
            impact="MEDIUM",
            confidence="HIGH",
        )
        ai_output = (
            "## Triage Finding Bảo Mật SEMGREP-001\n\n"
            "### 1. Phân loại\n\n"
            "True Positive"
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)

            report_path = triage.write_triage_outputs([record], {1: ai_output}, output_dir)

            report = report_path.read_text(encoding="utf-8")
            raw_ai_output = (
                output_dir / "findings" / "001_rule-one_ai_output.md"
            ).read_text(encoding="utf-8")

        self.assertNotIn("\n## Triage Finding Bảo Mật SEMGREP-001", report)
        self.assertNotIn("\n### 1. Phân loại", report)
        self.assertIn("\n##### Triage Finding Bảo Mật SEMGREP-001", report)
        self.assertIn("\n##### 1. Phân loại", report)
        self.assertIn("## Triage Finding Bảo Mật SEMGREP-001", raw_ai_output)

    def test_postman_mapping_extracts_api_url_template_literal_and_method(self):
        triage = load_triage_module()
        login_record = triage.FindingRecord(
            index=5,
            rule_id="typescript.react.security.react-insecure-request.react-insecure-request",
            file_path="frontend-mobile/App.js",
            line=189,
            severity="ERROR",
            message="Unencrypted request over HTTP detected.",
            code='const response = await fetch(`${API_URL}/login`, {\n  method: "POST",\n  headers: { "Content-Type": "application/json" },\n});',
            cwe="CWE-319",
            owasp="A02:2021",
            likelihood="LOW",
            impact="MEDIUM",
            confidence="MEDIUM",
        )
        orders_record = triage.FindingRecord(
            index=4,
            rule_id="typescript.react.security.react-insecure-request.react-insecure-request",
            file_path="frontend-mobile/App.js",
            line=174,
            severity="ERROR",
            message="Unencrypted request over HTTP detected.",
            code="const response = await fetch(`${API_URL}/orders/my-orders`, { headers: authHeaders });",
            cwe="CWE-319",
            owasp="A02:2021",
            likelihood="LOW",
            impact="MEDIUM",
            confidence="MEDIUM",
        )

        login_mapping = triage.runtime_mapping_for_record(login_record)
        orders_mapping = triage.runtime_mapping_for_record(orders_record)

        self.assertEqual(login_mapping.method, "POST")
        self.assertEqual(login_mapping.url, "http://localhost:3000/api/login")
        self.assertEqual(orders_mapping.method, "GET")
        self.assertEqual(
            orders_mapping.url,
            "http://localhost:3000/api/orders/my-orders",
        )

    def test_test_case_entries_mark_unknown_mapping_for_manual_review(self):
        triage = load_triage_module()
        record = triage.FindingRecord(
            index=3,
            rule_id="javascript.security.unknown-rule",
            file_path="backend/server.js",
            line=88,
            severity="WARNING",
            message="Potential security issue.",
            code="dangerousCall(userInput);",
            cwe="N/A",
            owasp="N/A",
            likelihood="N/A",
            impact="N/A",
            confidence="N/A",
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)

            triage.write_test_case_entries_report([record], output_dir)

            report = (output_dir / "semgrep_test_cases.md").read_text(
                encoding="utf-8"
            )

        self.assertIn("## TC-SEMGREP-003", report)
        self.assertIn("- Finding liên quan: SEMGREP-003", report)
        self.assertIn("http://localhost:3000/<map-endpoint>", report)
        self.assertIn("Chưa kiểm chứng", report)
        self.assertNotIn("### Expected output", report)
        self.assertNotIn("### Actual output", report)

    def test_main_stops_without_writing_reports_when_ai_call_fails(self):
        triage = load_triage_module()
        semgrep_json = {
            "results": [
                {
                    "check_id": "rule.one",
                    "path": "backend/server.js",
                    "start": {"line": 2},
                    "extra": {
                        "severity": "WARNING",
                        "message": "Hard-coded credential",
                        "lines": "const SECRET_KEY = 'secret';",
                        "metadata": {},
                    },
                }
            ]
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            json_path = tmp_path / "semgrep.json"
            output_dir = tmp_path / "output"
            json_path.write_text(json.dumps(semgrep_json), encoding="utf-8")
            settings = triage.AiSettings(
                provider="openai-compatible",
                model="test-model",
                api_key="test-key",
                base_url="https://example.test",
            )

            with mock.patch.object(triage, "get_ai_settings", return_value=settings):
                with mock.patch.object(
                    triage,
                    "generate_ai_response",
                    side_effect=RuntimeError("provider 402"),
                ):
                    with mock.patch.object(triage, "write_triage_outputs") as write_mock:
                        exit_code = triage.main(
                            [str(json_path), "--output-dir", str(output_dir)]
                        )

        self.assertEqual(exit_code, 1)
        write_mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
