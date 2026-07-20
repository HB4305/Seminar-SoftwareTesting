import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


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
        self.assertIn("Human Validation", report)
        self.assertIn("const SECRET_KEY", prompt)
        self.assertIn("AI output body", ai_output)

    def test_write_triage_outputs_creates_postman_validation_report(self):
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

            report = (output_dir / "semgrep_postman_validation_report.md").read_text(
                encoding="utf-8"
            )

        self.assertIn("## SEMGREP-001: Hardcoded JWT Secret", report)
        self.assertIn("### 4. Postman Test Case", report)
        self.assertIn("GET http://localhost:3000/api/users/me", report)
        self.assertIn("Authorization: Bearer <forged_admin_jwt>", report)
        self.assertIn("## SEMGREP-002: Insecure HTTP Request", report)
        self.assertIn("GET http://localhost:3000/api/products", report)
        self.assertIn("ZAP related alert", report)

    def test_postman_validation_report_marks_unknown_mapping_as_low_confidence(self):
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

            triage.write_postman_validation_report([record], output_dir)

            report = (output_dir / "semgrep_postman_validation_report.md").read_text(
                encoding="utf-8"
            )

        self.assertIn("## SEMGREP-003: Potential security issue", report)
        self.assertIn("Mapping confidence: Low", report)
        self.assertIn("http://localhost:3000/<map-endpoint>", report)


if __name__ == "__main__":
    unittest.main()
