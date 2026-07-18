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


if __name__ == "__main__":
    unittest.main()
