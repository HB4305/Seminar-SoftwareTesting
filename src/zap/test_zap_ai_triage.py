import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT_PATH = Path(__file__).with_name("zap_ai_triage.py")


def load_triage_module():
    spec = importlib.util.spec_from_file_location("src_zap_ai_triage", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ZapAiTriageWorkflowTest(unittest.TestCase):
    def test_collect_alert_records_flattens_instances_and_runtime_evidence(self):
        triage = load_triage_module()
        zap_json = {
            "@programName": "ZAP",
            "@version": "2.17.0",
            "@generated": "Wed, 22 Jul 2026 08:36:09",
            "site": [
                {
                    "@name": "http://localhost:3000",
                    "alerts": [
                        {
                            "pluginid": "10098",
                            "alertRef": "10098",
                            "alert": "Cross-Domain Misconfiguration",
                            "riskdesc": "Medium (Medium)",
                            "confidence": "2",
                            "cweid": "942",
                            "wascid": "14",
                            "desc": "<p>CORS policy permits broad access.</p>",
                            "solution": "<p>Restrict trusted origins.</p>",
                            "reference": "<p>https://www.zaproxy.org/</p>",
                            "tags": [{"tag": "OWASP_2021_A05", "link": ""}],
                            "instances": [
                                {
                                    "uri": "http://localhost:3000/api/users/me",
                                    "method": "GET",
                                    "param": "",
                                    "attack": "",
                                    "evidence": "Access-Control-Allow-Origin: *",
                                    "request-header": "GET http://localhost:3000/api/users/me HTTP/1.1\r\nHost: localhost:3000\r\n\r\n",
                                    "request-body": "",
                                    "response-header": "HTTP/1.1 200 OK\r\nAccess-Control-Allow-Origin: *\r\n\r\n",
                                    "response-body": "{\"id\":2,\"email\":\"test@eshop.com\"}",
                                }
                            ],
                        }
                    ],
                }
            ],
        }

        records = triage.collect_alert_records(zap_json, "backend_basic.json")

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].alert_id, "ZAP-001")
        self.assertEqual(records[0].plugin_id, "10098")
        self.assertEqual(records[0].alert_ref, "10098")
        self.assertEqual(records[0].alert_name, "Cross-Domain Misconfiguration")
        self.assertEqual(records[0].url, "http://localhost:3000/api/users/me")
        self.assertEqual(records[0].method, "GET")
        self.assertEqual(records[0].risk, "Medium")
        self.assertEqual(records[0].confidence, "Medium")
        self.assertEqual(records[0].cwe, "CWE-942")
        self.assertEqual(records[0].wasc, "WASC-14")
        self.assertIn("OWASP_2021_A05", records[0].tags)
        self.assertIn("Access-Control-Allow-Origin: *", records[0].response_header)

    def test_collect_alert_records_can_filter_target_prefixes(self):
        triage = load_triage_module()
        zap_json = {
            "site": [
                {
                    "@name": "https://external.example",
                    "alerts": [
                        {
                            "pluginid": "10035",
                            "alert": "Strict-Transport-Security Header Not Set",
                            "riskdesc": "Low (High)",
                            "instances": [{"uri": "https://external.example/a", "method": "GET"}],
                        }
                    ],
                },
                {
                    "@name": "http://localhost:3000",
                    "alerts": [
                        {
                            "pluginid": "10037",
                            "alert": "Server Leaks Information via X-Powered-By",
                            "riskdesc": "Low (Medium)",
                            "instances": [{"uri": "http://localhost:3000/api/login", "method": "POST"}],
                        }
                    ],
                },
            ]
        }

        records = triage.collect_alert_records(
            zap_json,
            "backend_basic.json",
            target_prefixes=["http://localhost:3000"],
        )

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].url, "http://localhost:3000/api/login")
        self.assertEqual(records[0].alert_id, "ZAP-001")

    def test_build_prompt_uses_runtime_context_not_source_context(self):
        triage = load_triage_module()
        record = triage.ZapAlertRecord(
            index=1,
            alert_id="ZAP-001",
            source_json="backend_basic.json",
            site="http://localhost:3000",
            plugin_id="10098",
            alert_ref="10098",
            alert_name="Cross-Domain Misconfiguration",
            risk="Medium",
            confidence="Medium",
            cwe="CWE-942",
            wasc="WASC-14",
            tags="OWASP_2021_A05",
            url="http://localhost:3000/api/users/me",
            method="GET",
            param="",
            attack="",
            evidence="Access-Control-Allow-Origin: *",
            request_header="GET http://localhost:3000/api/users/me HTTP/1.1\r\n\r\n",
            request_body="",
            response_header="HTTP/1.1 200 OK\r\nAccess-Control-Allow-Origin: *\r\n\r\n",
            response_body="{\"id\":2}",
            description="CORS policy permits broad access.",
            solution="Restrict trusted origins.",
            reference="https://www.zaproxy.org/",
        )

        prompt = triage.build_prompt(record)

        self.assertIn("Hãy trả lời hoàn toàn bằng tiếng Việt", prompt)
        self.assertIn("ZAP là DAST", prompt)
        self.assertIn("runtime evidence", prompt)
        self.assertIn("Request / bằng chứng request runtime", prompt)
        self.assertIn("Response / bằng chứng response runtime", prompt)
        self.assertIn("Phân loại: True Positive / False Positive / Needs Human Review", prompt)
        self.assertNotIn("source evidence", prompt)
        self.assertNotIn("mã nguồn", prompt)

    def test_extract_ai_classification_reads_first_classification_from_ai_output(self):
        triage = load_triage_module()

        true_positive = "## 1. Phân loại\n\n**True Positive**\n\nFalse Positive chỉ là trạng thái đối chiếu."
        needs_review = "1. **Phân loại:** Needs Human Review\n\nCần kiểm tra auth context."
        false_positive = "### Phân loại\nFalse Positive\n\nEvidence là cache busting timestamp."

        self.assertEqual(triage.extract_ai_classification(true_positive), "True Positive")
        self.assertEqual(triage.extract_ai_classification(needs_review), "Needs Human Review")
        self.assertEqual(triage.extract_ai_classification(false_positive), "False Positive")
        self.assertEqual(triage.extract_ai_classification(""), "Chưa có phân loại AI")

    def test_write_outputs_creates_semgrep_shaped_zap_reports(self):
        triage = load_triage_module()
        record = triage.ZapAlertRecord(
            index=1,
            alert_id="ZAP-001",
            source_json="backend_basic.json",
            site="http://localhost:3000",
            plugin_id="10098",
            alert_ref="10098",
            alert_name="Cross-Domain Misconfiguration",
            risk="Medium",
            confidence="Medium",
            cwe="CWE-942",
            wasc="WASC-14",
            tags="OWASP_2021_A05",
            url="http://localhost:3000/api/users/me",
            method="GET",
            param="",
            attack="",
            evidence="Access-Control-Allow-Origin: *",
            request_header="GET http://localhost:3000/api/users/me HTTP/1.1\r\nHost: localhost:3000\r\n\r\n",
            request_body="",
            response_header="HTTP/1.1 200 OK\r\nAccess-Control-Allow-Origin: *\r\n\r\n",
            response_body="{\"id\":2,\"email\":\"test@eshop.com\"}",
            description="CORS policy permits broad access.",
            solution="Restrict trusted origins.",
            reference="https://www.zaproxy.org/",
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)

            report_path = triage.write_triage_outputs(
                [record],
                {1: "## 1. Phân loại\n\nTrue Positive"},
                output_dir,
            )

            triage_report = report_path.read_text(encoding="utf-8")
            test_cases = (output_dir / "zap_test_cases.md").read_text(encoding="utf-8")
            prompt = (output_dir / "alerts" / "001_cross-domain-misconfiguration_prompt.md").read_text(
                encoding="utf-8"
            )
            ai_output = (
                output_dir / "alerts" / "001_cross-domain-misconfiguration_ai_output.md"
            ).read_text(encoding="utf-8")

        self.assertEqual(report_path.name, "zap_triage_report.md")
        self.assertIn("# Báo cáo ZAP AI Triage", triage_report)
        self.assertIn("## Bảng tổng hợp alerts", triage_report)
        self.assertIn(
            "| # | Alert | Endpoints | Risk | Confidence | CWE | WASC | Phân loại AI | Kết quả AI | Trạng thái kiểm chứng thủ công |",
            triage_report,
        )
        self.assertIn("| 1 | `Cross-Domain Misconfiguration` | 1 | Medium | Medium | CWE-942 | WASC-14 |", triage_report)
        self.assertIn("| 1 | `Cross-Domain Misconfiguration` | 1 | Medium | Medium | CWE-942 | WASC-14 | True Positive |", triage_report)
        self.assertIn("### ZAP-001: Cross-Domain Misconfiguration", triage_report)
        self.assertIn("#### Tags lỗi", triage_report)
        self.assertIn("| Plugin ID | `10098` |", triage_report)
        self.assertIn("#### Endpoints bị ảnh hưởng", triage_report)
        self.assertIn("| 1 | GET | `http://localhost:3000/api/users/me` | `` | `Access-Control-Allow-Origin: *` |", triage_report)
        self.assertIn("#### Bằng chứng runtime đại diện", triage_report)
        self.assertIn("```http\nGET http://localhost:3000/api/users/me", triage_report)
        self.assertIn("- Phân loại AI: True Positive", triage_report)
        self.assertIn("- Trạng thái kiểm chứng thủ công: Chưa kiểm chứng", triage_report)
        self.assertIn("##### 1. Phân loại", triage_report)
        self.assertIn("# Danh sách test case kiểm chứng ZAP", test_cases)
        self.assertIn("## TC-ZAP-001", test_cases)
        self.assertIn("- Alert liên quan: ZAP-001", test_cases)
        self.assertIn("- Source JSON: `backend_basic.json`", test_cases)
        self.assertIn("GET http://localhost:3000/api/users/me", test_cases)
        self.assertIn("Replay request theo method, URL, headers từ ZAP", test_cases)
        self.assertIn("Chưa kiểm chứng", test_cases)
        self.assertIn("ZAP là DAST", prompt)
        self.assertIn("True Positive", ai_output)

    def test_write_outputs_groups_triage_by_alert_and_keeps_all_test_cases(self):
        triage = load_triage_module()
        first_record = triage.ZapAlertRecord(
            index=1,
            alert_id="ZAP-001",
            source_json="backend_basic.json",
            site="http://localhost:3000",
            plugin_id="10098",
            alert_ref="10098",
            alert_name="Cross-Domain Misconfiguration",
            risk="Medium",
            confidence="Medium",
            cwe="CWE-942",
            wasc="WASC-14",
            tags="OWASP_2021_A05",
            url="http://localhost:3000",
            method="GET",
            param="N/A",
            attack="N/A",
            evidence="Access-Control-Allow-Origin: *",
            request_header="GET http://localhost:3000 HTTP/1.1\r\nHost: localhost:3000\r\n\r\n",
            request_body="",
            response_header="HTTP/1.1 200 OK\r\nAccess-Control-Allow-Origin: *\r\n\r\n",
            response_body="{}",
            description="CORS policy permits broad access.",
            solution="Restrict trusted origins.",
            reference="https://www.zaproxy.org/",
        )
        second_record = first_record._replace(
            index=2,
            alert_id="ZAP-002",
            url="http://localhost:3000/api/users/me",
            request_header="GET http://localhost:3000/api/users/me HTTP/1.1\r\nHost: localhost:3000\r\n\r\n",
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)

            report_path = triage.write_triage_outputs(
                [first_record, second_record],
                {1: "## 1. Phân loại\n\nTrue Positive"},
                output_dir,
            )

            triage_report = report_path.read_text(encoding="utf-8")
            test_cases = (output_dir / "zap_test_cases.md").read_text(encoding="utf-8")
            alerts_dir_files = sorted(path.name for path in (output_dir / "alerts").iterdir())

        self.assertIn("- Tổng số alert instance trong input: 2", triage_report)
        self.assertIn("- Tổng số alert sau khi gom nhóm: 1", triage_report)
        self.assertIn("| 1 | `Cross-Domain Misconfiguration` | 2 | Medium | Medium | CWE-942 | WASC-14 |", triage_report)
        self.assertEqual(triage_report.count("### ZAP-001: Cross-Domain Misconfiguration"), 1)
        self.assertNotIn("### ZAP-002: Cross-Domain Misconfiguration", triage_report)
        self.assertIn("| 1 | GET | `http://localhost:3000` | `N/A` | `Access-Control-Allow-Origin: *` |", triage_report)
        self.assertIn("| 2 | GET | `http://localhost:3000/api/users/me` | `N/A` | `Access-Control-Allow-Origin: *` |", triage_report)
        self.assertIn("## TC-ZAP-001", test_cases)
        self.assertIn("## TC-ZAP-002", test_cases)
        self.assertIn("- Alert liên quan: ZAP-001", test_cases)
        self.assertNotIn("- Alert liên quan: ZAP-002", test_cases)
        self.assertEqual(
            alerts_dir_files,
            [
                "001_cross-domain-misconfiguration_ai_output.md",
                "001_cross-domain-misconfiguration_prompt.md",
            ],
        )

    def test_main_offline_generates_reports_from_json_without_ai_key(self):
        triage = load_triage_module()
        zap_json = {
            "@version": "2.17.0",
            "site": [
                {
                    "@name": "http://localhost:3000",
                    "alerts": [
                        {
                            "pluginid": "10111",
                            "alertRef": "10111",
                            "alert": "Authentication Request Identified",
                            "riskdesc": "Informational (High)",
                            "confidence": "3",
                            "instances": [
                                {
                                    "uri": "http://localhost:3000/api/login",
                                    "method": "POST",
                                    "param": "email",
                                    "attack": "password",
                                    "evidence": "password",
                                    "request-header": "POST http://localhost:3000/api/login HTTP/1.1\r\nContent-Type: application/json\r\n\r\n",
                                    "request-body": "{\"email\":\"test@eshop.com\",\"password\":\"Test1234!\"}",
                                    "response-header": "HTTP/1.1 200 OK\r\n\r\n",
                                    "response-body": "{\"message\":\"Login successful\"}",
                                }
                            ],
                        }
                    ],
                }
            ],
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            json_path = tmp_path / "zap.json"
            output_dir = tmp_path / "output"
            json_path.write_text(json.dumps(zap_json), encoding="utf-8")

            exit_code = triage.main(
                [
                    str(json_path),
                    "--output-dir",
                    str(output_dir),
                    "--offline",
                    "--target-prefix",
                    "http://localhost:3000",
                ]
            )

            triage_report = (output_dir / "zap_triage_report.md").read_text(
                encoding="utf-8"
            )
            test_cases = (output_dir / "zap_test_cases.md").read_text(encoding="utf-8")

        self.assertEqual(exit_code, 0)
        self.assertIn("Authentication Request Identified", triage_report)
        self.assertIn("POST http://localhost:3000/api/login", test_cases)

    def test_collect_records_from_files_accepts_multiple_json_inputs_and_keeps_global_ids(self):
        triage = load_triage_module()
        first_json = {
            "site": [
                {
                    "@name": "http://localhost:3000",
                    "alerts": [
                        {
                            "pluginid": "10037",
                            "alert": "Server Leaks Information via X-Powered-By",
                            "riskdesc": "Low (Medium)",
                            "instances": [{"uri": "http://localhost:3000", "method": "GET"}],
                        }
                    ],
                }
            ]
        }
        second_json = {
            "site": [
                {
                    "@name": "http://localhost:5173",
                    "alerts": [
                        {
                            "pluginid": "10021",
                            "alert": "X-Content-Type-Options Header Missing",
                            "riskdesc": "Low (Medium)",
                            "instances": [{"uri": "http://localhost:5173/admin", "method": "GET"}],
                        }
                    ],
                }
            ]
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            first_path = tmp_path / "backend_basic.json"
            second_path = tmp_path / "frontend_admin_basic.json"
            first_path.write_text(json.dumps(first_json), encoding="utf-8")
            second_path.write_text(json.dumps(second_json), encoding="utf-8")

            records = triage.collect_records_from_files([first_path, second_path])

        self.assertEqual([record.alert_id for record in records], ["ZAP-001", "ZAP-002"])
        self.assertEqual(records[0].source_json, "backend_basic.json")
        self.assertEqual(records[1].source_json, "frontend_admin_basic.json")

    def test_get_ai_settings_prefers_openai_key_then_openrouter_key_and_raises_without_either(self):
        triage = load_triage_module()

        openai_settings = triage.get_ai_settings(
            {
                "AI_MODEL": "gpt-4.1-mini",
                "OPENAI_API_KEY": "openai-key",
                "OPENROUTER_API_KEY": "openrouter-key",
                "OPENAI_BASE_URL": "https://api.openai.com/v1",
            },
            env_file="",
        )
        openrouter_settings = triage.get_ai_settings(
            {
                "AI_MODEL": "openai/gpt-4.1-mini",
                "OPENROUTER_API_KEY": "openrouter-key",
                "OPENROUTER_BASE_URL": "https://openrouter.ai/api/v1",
            },
            env_file="",
        )

        self.assertEqual(openai_settings.provider, "openai-compatible")
        self.assertEqual(openai_settings.api_key, "openai-key")
        self.assertEqual(openai_settings.base_url, "https://api.openai.com/v1")
        self.assertEqual(openrouter_settings.api_key, "openrouter-key")
        self.assertEqual(openrouter_settings.base_url, "https://openrouter.ai/api/v1")
        with self.assertRaises(ValueError):
            triage.get_ai_settings({"AI_MODEL": "gpt-4.1-mini"}, env_file="")

    def test_get_ai_settings_supports_legacy_openrouter_model_and_chat_completions_url(self):
        triage = load_triage_module()

        settings = triage.get_ai_settings(
            {
                "OPENROUTER_MODEL": "google/gemini-2.5-flash",
                "OPENROUTER_API_KEY": "openrouter-key",
                "OPENROUTER_BASE_URL": "https://openrouter.ai/api/v1/chat/completions",
            },
            env_file="",
        )

        self.assertEqual(settings.model, "google/gemini-2.5-flash")
        self.assertEqual(settings.base_url, "https://openrouter.ai/api/v1")

    def test_generate_ai_response_posts_to_single_chat_completions_endpoint(self):
        triage = load_triage_module()
        settings = triage.AiSettings(
            provider="openai-compatible",
            model="google/gemini-2.5-flash",
            api_key="openrouter-key",
            base_url="https://openrouter.ai/api/v1",
            max_tokens=256,
        )
        captured = {}
        response = mock.Mock()
        response.__enter__ = mock.Mock(return_value=response)
        response.__exit__ = mock.Mock(return_value=None)
        response.read = mock.Mock(
            return_value=b'{"choices":[{"message":{"content":"triage ok"}}]}'
        )

        def fake_urlopen(request, timeout):
            captured["url"] = request.full_url
            captured["body"] = json.loads(request.data.decode("utf-8"))
            captured["timeout"] = timeout
            return response

        with mock.patch("urllib.request.urlopen", side_effect=fake_urlopen):
            result = triage.generate_ai_response("prompt", settings)

        self.assertEqual(result, "triage ok")
        self.assertEqual(
            captured["url"],
            "https://openrouter.ai/api/v1/chat/completions",
        )
        self.assertEqual(captured["body"]["model"], "google/gemini-2.5-flash")
        self.assertEqual(captured["body"]["max_tokens"], 256)


if __name__ == "__main__":
    unittest.main()
