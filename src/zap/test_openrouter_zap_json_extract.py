import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))

from openrouter_zap_json_extract import (
    DEFAULT_MODEL,
    ExtractedAlert,
    OpenRouterConfig,
    build_parser,
    build_prompt,
    call_openrouter,
    config_from_env,
    parse_zap_json_files,
    render_html,
    render_markdown,
)


class OpenRouterZapJsonExtractTests(unittest.TestCase):
    def test_parse_multiple_json_files_extracts_every_alert_instance_and_tags(self):
        report_one = {
            "site": [
                {
                    "@name": "http://localhost:3000",
                    "alerts": [
                        {
                            "alert": "SQL Injection",
                            "riskdesc": "High (Medium)",
                            "confidence": "Medium",
                            "desc": "<p>SQL injection description</p>",
                            "solution": "<p>Use parameterized queries</p>",
                            "cweid": "89",
                            "wascid": "19",
                            "tags": [
                                {"tag": "OWASP_2021_A03", "link": "https://owasp.org/Top10/A03_2021-Injection/"},
                                {"tag": "POLICY_PENTEST", "link": ""},
                            ],
                            "instances": [
                                {
                                    "uri": "http://localhost:3000/api/products?existing=1",
                                    "method": "GET",
                                    "param": "search",
                                    "attack": "' OR '1'='1",
                                    "evidence": "sql syntax error",
                                    "request-header": "GET http://localhost:3000/api/products?existing=1 HTTP/1.1\r\nhost: localhost:3000\r\n\r\n",
                                },
                                {
                                    "uri": "http://localhost:3000/api/login",
                                    "method": "POST",
                                    "param": "email",
                                    "attack": "admin'--",
                                    "request-body": "{\"email\":\"admin@test\",\"password\":\"x\"}",
                                },
                            ],
                        }
                    ],
                }
            ]
        }
        report_two = {
            "site": {
                "@name": "http://localhost:5173",
                "alerts": [
                    {
                        "name": "Content Security Policy Header Not Set",
                        "riskdesc": "Medium (High)",
                        "cweid": "693",
                        "wascid": "15",
                        "tags": {"OWASP_2021_A05": "https://owasp.org/Top10/A05_2021-Security_Misconfiguration/"},
                        "instances": [
                            {
                                "uri": "http://localhost:5173/",
                                "method": "GET",
                                "evidence": "Content-Security-Policy header missing",
                            }
                        ],
                    }
                ],
            }
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            first = Path(temp_dir) / "backend.json"
            second = Path(temp_dir) / "frontend.json"
            first.write_text(json.dumps(report_one), encoding="utf-8")
            second.write_text(json.dumps(report_two), encoding="utf-8")

            alerts = parse_zap_json_files([first, second])

        self.assertEqual(len(alerts), 3)
        self.assertEqual(alerts[0].source_file, "backend.json")
        self.assertEqual(alerts[0].alert_name, "SQL Injection")
        self.assertEqual(alerts[0].risk, "High")
        self.assertEqual(alerts[0].owasp_tags, ["OWASP_2021_A03"])
        self.assertFalse(hasattr(alerts[0], "cwe"))
        self.assertFalse(hasattr(alerts[0], "wasc"))
        self.assertFalse(hasattr(alerts[0], "tags"))
        self.assertEqual(alerts[0].poc["method"], "GET")
        self.assertEqual(alerts[0].poc["endpoint"], "http://localhost:3000/api/products?existing=1")
        self.assertEqual(alerts[0].poc["payload"], "' OR '1'='1")
        self.assertIn("search", alerts[0].poc["notes"])
        self.assertEqual(alerts[1].poc["method"], "POST")
        self.assertIn("admin'--", alerts[1].poc["payload"])
        self.assertEqual(alerts[2].owasp_tags, ["OWASP_2021_A05"])

    def test_build_prompt_contains_required_sections_for_ai(self):
        alert = ExtractedAlert(
            source_file="backend.json",
            site="http://localhost:3000",
            alert_name="Cross-Domain Misconfiguration",
            risk="Medium",
            confidence="Medium",
            method="GET",
            endpoint="http://localhost:3000/api/products",
            parameter="Access-Control-Allow-Origin",
            attack="",
            evidence="Access-Control-Allow-Origin: *",
            description="CORS is too permissive.",
            solution="Restrict allowed origins.",
            owasp_tags=["OWASP_2021_A01"],
            request_header="",
            request_body="",
            response_header="",
            response_body="",
            poc={
                "method": "GET",
                "endpoint": "http://localhost:3000/api/products",
                "payload": "",
                "notes": "Send Origin header and inspect Access-Control-Allow-Origin.",
            },
        )

        prompt = build_prompt([alert], ["backend.json"])

        self.assertIn("Chi tiết + giải thích lỗi", prompt)
        self.assertIn("Tag OWASP", prompt)
        self.assertIn("PoC", prompt)
        self.assertIn("Cách verify PoC", prompt)
        self.assertIn("Cross-Domain Misconfiguration", prompt)
        self.assertIn("OWASP_2021_A01", prompt)
        self.assertNotIn("CWE-264", prompt)
        self.assertNotIn("WASC", prompt)
        self.assertIn("GET http://localhost:3000/api/products", prompt)

    def test_config_from_env_requires_api_key(self):
        old_key = os.environ.pop("OPENROUTER_API_KEY", None)
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                missing_env = Path(temp_dir) / ".env"
                with self.assertRaisesRegex(RuntimeError, "OPENROUTER_API_KEY"):
                    config_from_env(missing_env)
        finally:
            if old_key is not None:
                os.environ["OPENROUTER_API_KEY"] = old_key

    def test_config_from_env_reads_openrouter_values(self):
        previous = {
            key: os.environ.get(key)
            for key in (
                "OPENROUTER_API_KEY",
                "OPENROUTER_MODEL",
                "OPENROUTER_BASE_URL",
                "OPENROUTER_TIMEOUT",
                "OPENROUTER_MAX_TOKENS",
            )
        }
        try:
            os.environ["OPENROUTER_API_KEY"] = "test-key"
            os.environ["OPENROUTER_MODEL"] = "google/gemini-2.5-pro"
            os.environ["OPENROUTER_BASE_URL"] = "https://example.test/chat"
            os.environ["OPENROUTER_TIMEOUT"] = "7"
            os.environ["OPENROUTER_MAX_TOKENS"] = "4096"

            with tempfile.TemporaryDirectory() as temp_dir:
                missing_env = Path(temp_dir) / ".env"
                config = config_from_env(missing_env)

            self.assertEqual(config.api_key, "test-key")
            self.assertEqual(config.model, "google/gemini-2.5-pro")
            self.assertEqual(config.base_url, "https://example.test/chat")
            self.assertEqual(config.timeout, 7)
            self.assertEqual(config.max_tokens, 4096)
        finally:
            for key, value in previous.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value

    def test_render_markdown_and_html_include_ai_result(self):
        markdown = render_markdown(
            ai_text="## Finding\n- safe text",
            source_names=["backend.json", "frontend.json"],
            model="google/gemini-2.5-flash",
        )
        html = render_html(
            ai_text="<script>alert(1)</script>\n## Finding",
            source_names=["backend.json"],
            model="google/gemini-2.5-flash",
        )

        self.assertIn("# ZAP OpenRouter JSON Extract Result", markdown)
        self.assertIn("backend.json", markdown)
        self.assertIn("frontend.json", markdown)
        self.assertIn("## Finding", markdown)
        self.assertIn("<!doctype html>", html)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", html)
        self.assertNotIn("<script>alert(1)</script>", html)

    def test_parser_accepts_multiple_inputs_and_required_output_options(self):
        parser = build_parser()

        args = parser.parse_args(
            [
                "--input",
                "src/zap/output/backend_basic.json",
                "src/zap/output/frontend_user_basic.json",
                "--format",
                "html",
                "--output",
                "src/zap/output/result.html",
            ]
        )

        self.assertEqual(args.input, ["src/zap/output/backend_basic.json", "src/zap/output/frontend_user_basic.json"])
        self.assertEqual(args.format, "html")
        self.assertEqual(args.output, "src/zap/output/result.html")
        self.assertEqual(DEFAULT_MODEL, "google/gemini-2.5-flash")

    def test_call_openrouter_sends_configured_max_tokens(self):
        captured = {}

        class FakeResponse:
            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, traceback):
                return False

            def read(self):
                return json.dumps({"choices": [{"message": {"content": "AI result"}}]}).encode("utf-8")

        def fake_urlopen(request, timeout):
            captured["timeout"] = timeout
            captured["body"] = json.loads(request.data.decode("utf-8"))
            return FakeResponse()

        config = OpenRouterConfig(
            api_key="test-key",
            model="google/gemini-2.5-flash",
            base_url="https://example.test/chat",
            timeout=9,
            max_tokens=2048,
        )

        with patch("openrouter_zap_json_extract.urllib.request.urlopen", fake_urlopen):
            result = call_openrouter("prompt text", config)

        self.assertEqual(result, "AI result")
        self.assertEqual(captured["timeout"], 9)
        self.assertEqual(captured["body"]["max_tokens"], 2048)
        self.assertEqual(captured["body"]["model"], "google/gemini-2.5-flash")


if __name__ == "__main__":
    unittest.main()
