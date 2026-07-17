import os
import re
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))

from zap_runtime import (
    CONTEXT_REGEX,
    Credential,
    ZapDockerManager,
    get_credential,
    validate_target,
)


class ZapRuntimeTests(unittest.TestCase):
    def test_validate_target_accepts_eshop_local_ports(self):
        for url in (
            "http://localhost:3000",
            "http://localhost:5173/",
            "http://127.0.0.1:5174/admin",
        ):
            with self.subTest(url=url):
                self.assertEqual(validate_target(url), url)

    def test_validate_target_rejects_external_or_unknown_port(self):
        for url in ("https://example.com", "http://localhost:8080"):
            with self.subTest(url=url):
                with self.assertRaisesRegex(ValueError, "local EShop"):
                    validate_target(url)

    def test_validate_target_rejects_malformed_port_with_friendly_error(self):
        with self.assertRaisesRegex(ValueError, "local EShop"):
            validate_target("http://localhost:abc")

    def test_context_regex_matches_eshop_target_scope(self):
        for url in (
            "http://localhost:3000",
            "http://localhost:3000/",
            "http://localhost:3000?x=1",
            "http://127.0.0.1:5174/admin#section",
        ):
            with self.subTest(url=url):
                self.assertIsNotNone(re.fullmatch(CONTEXT_REGEX, url))

    def test_context_regex_rejects_external_or_unknown_targets(self):
        for url in (
            "http://localhost:3000.evil.test/path",
            "https://localhost:3000",
            "http://localhost:8080",
        ):
            with self.subTest(url=url):
                self.assertIsNone(re.search(CONTEXT_REGEX, url))

    def test_get_credential_uses_seed_user(self):
        self.assertEqual(
            get_credential("user"),
            Credential("test@eshop.com", "Test1234!"),
        )

    @patch.dict(
        os.environ,
        {"ZAP_ADMIN_EMAIL": "scan-admin@example.test", "ZAP_ADMIN_PASSWORD": "secret"},
        clear=False,
    )
    def test_get_credential_allows_environment_override(self):
        self.assertEqual(
            get_credential("admin"),
            Credential("scan-admin@example.test", "secret"),
        )

    def test_get_credential_returns_none_for_anonymous(self):
        self.assertIsNone(get_credential("none"))

    @patch("zap_runtime.subprocess.run")
    def test_docker_manager_starts_expected_container(self, run):
        run.return_value.returncode = 0
        manager = ZapDockerManager(port=8090, container_name="test-zap")

        manager.start()

        run.assert_any_call(["docker", "version"], check=True, capture_output=True, text=True)
        run.assert_any_call(
            [
                "docker", "run", "--rm", "-d", "--name", "test-zap",
                "--network", "host", "ghcr.io/zaproxy/zaproxy:stable",
                "zap.sh", "-daemon", "-port", "8090", "-host", "0.0.0.0",
                "-config", "api.disablekey=true",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertTrue(manager.started)

    @patch("zap_runtime.subprocess.run")
    def test_docker_manager_stops_only_after_start(self, run):
        manager = ZapDockerManager(container_name="test-zap")
        manager.stop()
        run.assert_not_called()

        manager.started = True
        manager.stop()
        run.assert_called_once_with(
            ["docker", "stop", "test-zap"],
            check=False,
            capture_output=True,
            text=True,
        )
