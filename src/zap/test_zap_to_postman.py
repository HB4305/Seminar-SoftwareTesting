import json
import unittest
from pathlib import Path
import tempfile
import os
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from zap_to_postman import parse_zap_report, generate_postman_item


class ZapToPostmanTests(unittest.TestCase):
    def test_parse_zap_report_extracts_correct_fields(self):
        sample_zap_json = {
            "site": [
                {
                    "@name": "http://localhost:3000",
                    "alerts": [
                        {
                            "alert": "SQL Injection",
                            "cweid": "89",
                            "tags": {
                                "OWASP_2021_A03": "https://owasp.org/Top10/A03_2021-Injection/"
                            },
                            "desc": "SQL injection description",
                            "solution": "Use parameterized queries",
                            "instances": [
                                {
                                    "uri": "http://localhost:3000/api/products",
                                    "method": "GET",
                                    "param": "search",
                                    "attack": "' OR '1'='1",
                                    "evidence": "error in sql syntax"
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = Path(temp_dir) / "zap_report.json"
            temp_file.write_text(json.dumps(sample_zap_json), encoding="utf-8")

            alerts = parse_zap_report(temp_file)
            self.assertEqual(len(alerts), 1)
            
            alert = alerts[0]
            self.assertEqual(alert["alert_name"], "SQL Injection")
            self.assertEqual(alert["cwe"], "CWE-89")
            self.assertEqual(alert["owasp"], "OWASP_2021_A03")
            self.assertEqual(alert["uri"], "http://localhost:3000/api/products")
            self.assertEqual(alert["method"], "GET")
            self.assertEqual(alert["param"], "search")
            self.assertEqual(alert["attack"], "' OR '1'='1")

    def test_generate_postman_item_builds_valid_get_request(self):
        alert_data = {
            "alert_name": "SQL Injection",
            "cwe": "CWE-89",
            "owasp": "OWASP_2021_A03",
            "uri": "http://localhost:3000/api/products?existing=val",
            "method": "GET",
            "param": "search",
            "attack": "' OR '1'='1",
            "evidence": "sql syntax",
            "description": "SQL Injection description",
            "solution": "Fix SQL"
        }

        item = generate_postman_item(alert_data)
        
        self.assertIn("SQL Injection", item["name"])
        request = item["request"]
        self.assertEqual(request["method"], "GET")
        self.assertEqual(request["url"]["protocol"], "http")
        self.assertEqual(request["url"]["port"], "3000")
        self.assertEqual(request["url"]["host"], ["localhost"])
        self.assertEqual(request["url"]["path"], ["api", "products"])
        
        # Check query parameters (should merge existing and attack parameters)
        query = request["url"]["query"]
        query_dict = {q["key"]: q["value"] for q in query}
        self.assertEqual(query_dict["existing"], "val")
        self.assertEqual(query_dict["search"], "' OR '1'='1")
        self.assertIn("search=%27+OR+%271%27%3D%271", request["url"]["raw"])

    def test_generate_postman_item_builds_valid_post_request(self):
        alert_data = {
            "alert_name": "SQL Injection",
            "cwe": "CWE-89",
            "owasp": "OWASP_2021_A03",
            "uri": "http://localhost:3000/api/login",
            "method": "POST",
            "param": "username",
            "attack": "admin'--",
            "evidence": "",
            "description": "SQL injection",
            "solution": "Use parameterized query"
        }

        item = generate_postman_item(alert_data)
        request = item["request"]
        self.assertEqual(request["method"], "POST")
        self.assertEqual(request["body"]["mode"], "raw")
        
        body_json = json.loads(request["body"]["raw"])
        self.assertEqual(body_json["username"], "admin'--")
        
        # Check description content
        desc = request["description"]
        self.assertIn("OWASP Category: OWASP_2021_A03", desc)
        self.assertIn("CWE: CWE-89", desc)


if __name__ == "__main__":
    unittest.main()
