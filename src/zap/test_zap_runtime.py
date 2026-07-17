import contextlib
import io
import json
import os
import re
import subprocess
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
    login_for_token,
    validate_target,
    verify_authenticated_session,
)


class FakeResponse:
    def __init__(self, payload, status=200):
        self.payload = json.dumps(payload).encode("utf-8")
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return self.payload


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

    @patch("zap_runtime.urllib.request.build_opener")
    def test_login_for_token_extracts_jwt_without_logging_it(self, build_opener):
        build_opener.return_value.open.return_value = FakeResponse({"token": "jwt-value"})
        stdout = io.StringIO()
        stderr = io.StringIO()

        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            token = login_for_token(
                "http://localhost:8090",
                Credential("a@b.test", "secret"),
            )

        self.assertEqual(token, "jwt-value")
        self.assertNotIn("jwt-value", stdout.getvalue())
        self.assertNotIn("jwt-value", stderr.getvalue())

    @patch("zap_runtime.urllib.request.build_opener")
    def test_login_for_token_rejects_missing_token(self, build_opener):
        build_opener.return_value.open.return_value = FakeResponse({"message": "ok"})

        with self.assertRaisesRegex(RuntimeError, "token"):
            login_for_token("http://localhost:8090", Credential("a@b.test", "secret"))

    @patch("zap_runtime.urllib.request.build_opener")
    def test_verify_authenticated_session_requires_success(self, build_opener):
        build_opener.return_value.open.return_value = FakeResponse(
            {"email": "a@b.test"},
            status=200,
        )

        verify_authenticated_session("http://localhost:8090")

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

    @patch("zap_runtime.subprocess.run")
    def test_docker_manager_reports_missing_docker(self, run):
        run.side_effect = FileNotFoundError("docker")
        manager = ZapDockerManager(container_name="test-zap")

        with self.assertRaisesRegex(RuntimeError, "Docker must be installed/running") as raised:
            manager.start()

        self.assertIn("docker version", str(raised.exception))
        self.assertFalse(manager.started)

    @patch("zap_runtime.subprocess.run")
    def test_docker_manager_reports_docker_version_failure(self, run):
        run.side_effect = subprocess.CalledProcessError(
            1,
            ["docker", "version"],
            stderr="Cannot connect to the Docker daemon",
        )
        manager = ZapDockerManager(container_name="test-zap")

        with self.assertRaisesRegex(RuntimeError, "Docker must be installed/running") as raised:
            manager.start()

        message = str(raised.exception)
        self.assertIn("docker version", message)
        self.assertIn("Cannot connect to the Docker daemon", message)
        self.assertFalse(manager.started)

    @patch("zap_runtime.subprocess.run")
    def test_docker_manager_reports_docker_run_failure(self, run):
        run.side_effect = [
            subprocess.CompletedProcess(["docker", "version"], 0),
            subprocess.CalledProcessError(
                125,
                ["docker", "run"],
                stderr="port is already allocated",
            ),
        ]
        manager = ZapDockerManager(container_name="test-zap")

        with self.assertRaisesRegex(RuntimeError, "Docker must be installed/running") as raised:
            manager.start()

        message = str(raised.exception)
        self.assertIn("docker run", message)
        self.assertIn("port is already allocated", message)
        self.assertFalse(manager.started)
