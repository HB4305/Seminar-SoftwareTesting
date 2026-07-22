import json
import os
import shutil
import subprocess
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
RULES_PATH = REPO_ROOT / "src" / "semgrep" / "rules" / "eshop-security.yml"
SOURCE_ROOT = REPO_ROOT / "eshop-sut"
SOURCE_FILES = [
    SOURCE_ROOT / "backend" / "database.js",
    SOURCE_ROOT / "backend" / "server.js",
    SOURCE_ROOT / "backend" / "test_profile.js",
    SOURCE_ROOT / "frontend-admin" / "src" / "App.jsx",
    SOURCE_ROOT / "frontend-admin" / "src" / "main.jsx",
    SOURCE_ROOT / "frontend-mobile" / "App.js",
    SOURCE_ROOT / "frontend-mobile" / "index.js",
    SOURCE_ROOT / "frontend-web" / "src" / "App.jsx",
    SOURCE_ROOT / "frontend-web" / "src" / "context" / "AuthContext.jsx",
    SOURCE_ROOT / "frontend-web" / "src" / "context" / "CartContext.jsx",
    SOURCE_ROOT / "frontend-web" / "src" / "main.jsx",
    SOURCE_ROOT / "frontend-web" / "src" / "pages" / "Cart.jsx",
    SOURCE_ROOT / "frontend-web" / "src" / "pages" / "Checkout.jsx",
    SOURCE_ROOT / "frontend-web" / "src" / "pages" / "ForgotPassword.jsx",
    SOURCE_ROOT / "frontend-web" / "src" / "pages" / "Home.jsx",
    SOURCE_ROOT / "frontend-web" / "src" / "pages" / "Login.jsx",
    SOURCE_ROOT / "frontend-web" / "src" / "pages" / "ProductDetail.jsx",
    SOURCE_ROOT / "frontend-web" / "src" / "pages" / "Profile.jsx",
    SOURCE_ROOT / "frontend-web" / "src" / "pages" / "Register.jsx",
]


class EshopCustomRulesTest(unittest.TestCase):
    def test_custom_rules_cover_eshop_security_patterns(self):
        semgrep = shutil.which("semgrep")
        if not semgrep:
            self.skipTest("semgrep CLI is not installed")

        self.assertTrue(RULES_PATH.exists(), "Missing EShop custom Semgrep rules")

        env = os.environ.copy()
        env["HOME"] = "/private/tmp/semgrep-home"
        env["SSL_CERT_FILE"] = "/etc/ssl/cert.pem"
        env["SEMGREP_SEND_METRICS"] = "off"
        env["OTEL_SDK_DISABLED"] = "true"

        result = subprocess.run(
            [
                semgrep,
                "scan",
                "--disable-version-check",
                "--config",
                str(RULES_PATH),
                "--metrics",
                "off",
                "--json",
                "--quiet",
                *(str(path) for path in SOURCE_FILES),
            ],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            env=env,
            timeout=60,
        )

        self.assertEqual(
            result.returncode,
            0,
            f"Semgrep custom rules failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}",
        )

        data = json.loads(result.stdout)
        rule_ids = {
            finding["check_id"].removeprefix("src.semgrep.rules.")
            for finding in data.get("results", [])
        }
        expected_rule_ids = {
            "eshop.jwt.hardcoded-secret-constant",
            "eshop.backend.plaintext-password-storage",
            "eshop.backend.sql-template-string",
            "eshop.frontend.cleartext-http-url",
            "eshop.frontend.dangerously-set-inner-html",
            "eshop.frontend.localstorage-token",
            "eshop.backend.admin-route-missing-role-check",
            "eshop.backend.trusts-client-total-amount",
        }

        missing = expected_rule_ids - rule_ids
        self.assertFalse(missing, f"Expected custom rules did not match: {missing}")


if __name__ == "__main__":
    unittest.main()
