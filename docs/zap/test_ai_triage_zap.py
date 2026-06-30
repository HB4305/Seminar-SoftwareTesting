import os
import tempfile
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ai_triage_zap import (
    Alert,
    DEFAULT_MODEL,
    build_offline_triage,
    load_dotenv,
    parse_zap_html,
    render_markdown,
    resolve_output_path,
    update_submission_file,
)


SAMPLE_REPORT = """
<html>
<body>
<h1>ZAP Scanning Report</h1>
<table>
  <tr>
    <td><a href="#alert-1">Cross Site Scripting (DOM Based)</a></td>
    <td align="center" class="risk-3">High</td>
    <td align="center">High</td>
    <td>GET http://localhost:5173/?name=abc#&lt;img src=&quot;x&quot; onerror=alert(1)&gt;</td>
    <td>Parameter: name</td>
    <td>Evidence: &lt;img src=&quot;x&quot; onerror=alert(1)&gt;</td>
    <td>Solution: Encode output before rendering user-controlled values.</td>
  </tr>
</table>
</body>
</html>
"""

CLASSIC_REPORT = """
<html><body>
<table class="results">
  <tr>
    <th class="risk-2"><a id="10098"></a><div>Medium</div></th>
    <th class="risk-2">Cross-Domain Misconfiguration</th>
  </tr>
  <tr><td>Description</td><td><div>CORS is too permissive.</div></td></tr>
  <tr><td class="indent1">URL</td><td><a href="http://localhost:3000/api/products?search=">http://localhost:3000/api/products?search=</a></td></tr>
  <tr><td class="indent2">Method</td><td>GET</td></tr>
  <tr><td class="indent2">Parameter</td><td>Access-Control-Allow-Origin</td></tr>
  <tr><td class="indent2">Evidence</td><td>Access-Control-Allow-Origin: *</td></tr>
  <tr><td>Solution</td><td>Configure a restrictive set of domains.</td></tr>
</table>
</body></html>
"""


class AiTriageZapTests(unittest.TestCase):
    def test_parse_zap_html_extracts_alert_from_table_report(self):
        alerts = parse_zap_html(SAMPLE_REPORT)

        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0].name, "Cross Site Scripting (DOM Based)")
        self.assertEqual(alerts[0].risk, "High")
        self.assertEqual(alerts[0].confidence, "High")
        self.assertEqual(alerts[0].method, "GET")
        self.assertEqual(alerts[0].url, "http://localhost:5173/?name=abc#<img src=\"x\" onerror=alert(1)>")
        self.assertEqual(alerts[0].parameter, "name")
        self.assertIn("onerror=alert(1)", alerts[0].evidence)

    def test_offline_triage_includes_poc_and_testcase_for_xss(self):
        alert = Alert(
            name="Cross Site Scripting (DOM Based)",
            risk="High",
            confidence="High",
            method="GET",
            url="http://localhost:5173/?name=abc#<img src=\"x\" onerror=alert(1)>",
            parameter="name",
            evidence="<img src=\"x\" onerror=alert(1)>",
            solution="Encode output before rendering user-controlled values.",
        )

        triage = build_offline_triage([alert], source_name="sample.html")

        self.assertIn("DOM XSS", triage)
        self.assertIn("PoC", triage)
        self.assertIn("Testcase", triage)
        self.assertIn("http://localhost:5173/?name=abc", triage)

    def test_parse_zap_html_extracts_alert_from_classic_report(self):
        alerts = parse_zap_html(CLASSIC_REPORT)

        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0].name, "Cross-Domain Misconfiguration")
        self.assertEqual(alerts[0].risk, "Medium")
        self.assertEqual(alerts[0].method, "GET")
        self.assertEqual(alerts[0].url, "http://localhost:3000/api/products?search=")
        self.assertEqual(alerts[0].parameter, "Access-Control-Allow-Origin")
        self.assertEqual(alerts[0].evidence, "Access-Control-Allow-Origin: *")

    def test_render_markdown_contains_submission_ready_section(self):
        alert = Alert(
            name="Content Security Policy (CSP) Header Not Set",
            risk="Medium",
            confidence="High",
            method="GET",
            url="http://localhost:5173/robots.txt",
            parameter="",
            evidence="",
            solution="Set Content-Security-Policy.",
        )

        markdown = render_markdown(
            alerts=[alert],
            triage_text="AI triage content",
            source_name="zap_report.html",
            model_name="offline-template",
        )

        self.assertIn("# ZAP AI Triage Report", markdown)
        self.assertIn("## Submission Block", markdown)
        self.assertIn("AI triage content", markdown)
        self.assertIn("Content Security Policy", markdown)

    def test_load_dotenv_reads_key_from_env_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            env_path = Path(temp_dir) / ".env"
            env_path.write_text("GEMINI_API_KEY=test-key\n", encoding="utf-8")
            os.environ.pop("GEMINI_API_KEY", None)
            try:
                load_dotenv(env_path)
                self.assertEqual(os.environ["GEMINI_API_KEY"], "test-key")
            finally:
                os.environ.pop("GEMINI_API_KEY", None)

    def test_default_model_uses_supported_gemini_model(self):
        self.assertEqual(DEFAULT_MODEL, "gemini-2.5-flash")

    def test_resolve_output_path_uses_report_stem(self):
        report_path = Path("docs/zap/output/backend_report.html")
        output_path = resolve_output_path(report_path, None)

        self.assertEqual(output_path, Path("docs/zap/output/backend_report_ai_triage.md"))

    def test_update_submission_file_replaces_managed_block(self):
        path = Path(__file__).resolve().parent / "_tmp_submission.md"
        try:
            path.write_text("Before\n<!-- ZAP_AI_TRIAGE_START -->\nold\n<!-- ZAP_AI_TRIAGE_END -->\nAfter\n", encoding="utf-8")
            update_submission_file(path, "new content")

            content = path.read_text(encoding="utf-8")

            self.assertIn("Before", content)
            self.assertIn("new content", content)
            self.assertNotIn("\nold\n", content)
            self.assertIn("After", content)
        finally:
            if path.exists():
                path.unlink()


if __name__ == "__main__":
    unittest.main()
