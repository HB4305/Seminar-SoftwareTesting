import contextlib
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, call, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))

from zap_runtime import (
    CONTEXT_REGEX,
    Credential,
    REPLACER_RULE,
    ZapDockerManager,
    cleanup_authenticated_context,
    configure_authenticated_context,
    ensure_context,
    get_credential,
    load_dotenv,
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

    def test_load_dotenv_reads_env_file_without_overriding_existing_values(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            env_path = Path(temp_dir) / ".env"
            env_path.write_text(
                "\n".join(
                    [
                        "# local ZAP config",
                        "ZAP_TARGET=http://localhost:5173",
                        "ZAP_AUTH_ROLE=user",
                        "ZAP_USER_PASSWORD='from-file'",
                    ]
                ),
                encoding="utf-8",
            )
            os.environ.pop("ZAP_TARGET", None)
            os.environ["ZAP_USER_PASSWORD"] = "from-env"
            try:
                load_dotenv(env_path)

                self.assertEqual(os.environ["ZAP_TARGET"], "http://localhost:5173")
                self.assertEqual(os.environ["ZAP_AUTH_ROLE"], "user")
                self.assertEqual(os.environ["ZAP_USER_PASSWORD"], "from-env")
            finally:
                os.environ.pop("ZAP_TARGET", None)
                os.environ.pop("ZAP_AUTH_ROLE", None)
                os.environ.pop("ZAP_USER_PASSWORD", None)

    def test_configure_authenticated_context_creates_scoped_user_and_replacer(self):
        zap = MagicMock()
        zap.context.context_list = []
        zap.context.new_context.return_value = "7"
        zap.users.users_list.return_value = []
        zap.users.new_user.return_value = "3"

        state = configure_authenticated_context(
            zap, Credential("test@eshop.com", "secret"), "jwt-value", forced_user=True
        )

        self.assertEqual(state.context_id, "7")
        self.assertEqual(state.user_id, "3")
        zap.context.include_in_context.assert_called_once_with("EShop", CONTEXT_REGEX)
        zap.context.set_context_in_scope.assert_called_once_with("EShop", "true")
        zap.users.set_user_enabled.assert_called_once_with("7", "3", "true")
        zap.replacer.add_rule.assert_called_once_with(
            REPLACER_RULE,
            "true",
            "REQ_HEADER",
            "false",
            "Authorization",
            "Bearer jwt-value",
            url=CONTEXT_REGEX,
        )
        zap.forcedUser.set_forced_user.assert_called_once_with("7", "3")
        zap.forcedUser.set_forced_user_mode_enabled.assert_called_once_with("true")

    def test_ensure_context_resets_existing_context_to_local_allowlist(self):
        zap = MagicMock()
        zap.context.context_list = ["EShop"]
        zap.context.context.return_value = {"id": "7"}
        zap.context.include_regexs.return_value = [".*"]

        context_id = ensure_context(zap)

        self.assertEqual(context_id, "7")
        zap.context.set_context_regexs.assert_called_once_with(
            "EShop", json.dumps([CONTEXT_REGEX]), "[]"
        )
        zap.context.include_in_context.assert_not_called()
        zap.context.set_context_in_scope.assert_called_once_with("EShop", "true")

    def test_ensure_context_keeps_existing_exact_local_allowlist(self):
        zap = MagicMock()
        zap.context.context_list = ["EShop"]
        zap.context.context.return_value = {"id": "7"}
        zap.context.include_regexs.return_value = [CONTEXT_REGEX]

        context_id = ensure_context(zap)

        self.assertEqual(context_id, "7")
        zap.context.set_context_regexs.assert_not_called()
        zap.context.include_in_context.assert_not_called()
        zap.context.set_context_in_scope.assert_called_once_with("EShop", "true")

    def test_configure_authenticated_context_requires_replacer_api(self):
        zap = MagicMock()
        zap.context.context_list = []
        zap.context.new_context.return_value = "7"
        zap.users.users_list.return_value = []
        zap.users.new_user.return_value = "3"
        zap.replacer.add_rule.side_effect = Exception("missing replacer")

        with self.assertRaisesRegex(RuntimeError, "Replacer"):
            configure_authenticated_context(
                zap,
                Credential("test@eshop.com", "secret"),
                "jwt-value",
                forced_user=False,
            )

        zap.forcedUser.set_forced_user_mode_enabled.assert_not_called()

    def test_configure_authenticated_context_removes_replacer_when_forced_user_fails(self):
        zap = MagicMock()
        zap.context.context_list = []
        zap.context.new_context.return_value = "7"
        zap.users.users_list.return_value = []
        zap.users.new_user.return_value = "3"
        zap.forcedUser.set_forced_user.side_effect = Exception("forced user unavailable")

        with self.assertRaisesRegex(RuntimeError, "forced user setup failed") as raised:
            configure_authenticated_context(
                zap,
                Credential("test@eshop.com", "secret"),
                "jwt-value",
                forced_user=True,
            )

        self.assertIsInstance(raised.exception.__cause__, Exception)
        zap.replacer.add_rule.assert_called_once_with(
            REPLACER_RULE,
            "true",
            "REQ_HEADER",
            "false",
            "Authorization",
            "Bearer jwt-value",
            url=CONTEXT_REGEX,
        )
        self.assertEqual(
            zap.replacer.method_calls,
            [
                call.remove_rule(REPLACER_RULE),
                call.add_rule(
                    REPLACER_RULE,
                    "true",
                    "REQ_HEADER",
                    "false",
                    "Authorization",
                    "Bearer jwt-value",
                    url=CONTEXT_REGEX,
                ),
                call.remove_rule(REPLACER_RULE),
            ],
        )

    def test_cleanup_removes_secret_and_disables_forced_user(self):
        zap = MagicMock()
        cleanup_authenticated_context(zap, forced_user=True)
        zap.replacer.remove_rule.assert_called_once_with(REPLACER_RULE)
        zap.forcedUser.set_forced_user_mode_enabled.assert_called_once_with("false")

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
    def test_login_for_token_rejects_non_object_json_response(self, build_opener):
        build_opener.return_value.open.return_value = FakeResponse(["jwt-value"])

        with self.assertRaisesRegex(RuntimeError, "token"):
            login_for_token("http://localhost:8090", Credential("a@b.test", "secret"))

    def test_login_for_token_sends_login_request_through_zap_proxy(self):
        zap_url = "http://localhost:8090"
        with (
            patch("zap_runtime.urllib.request.ProxyHandler") as proxy_handler,
            patch("zap_runtime.urllib.request.build_opener") as build_opener,
        ):
            build_opener.return_value.open.return_value = FakeResponse({"token": "jwt-value"})

            login_for_token(
                zap_url,
                Credential("a@b.test", "secret"),
                timeout=9,
            )

        proxy_handler.assert_called_once_with({"http": zap_url, "https": zap_url})
        build_opener.assert_called_once_with(proxy_handler.return_value)
        open_call = build_opener.return_value.open.call_args
        request = open_call.args[0]
        self.assertEqual(request.full_url, "http://localhost:3000/api/login")
        self.assertEqual(request.get_method(), "POST")
        self.assertEqual(
            json.loads(request.data.decode("utf-8")),
            {"email": "a@b.test", "password": "secret"},
        )
        self.assertEqual(open_call.kwargs["timeout"], 9)

    @patch("zap_runtime.urllib.request.build_opener")
    def test_verify_authenticated_session_requires_success(self, build_opener):
        build_opener.return_value.open.return_value = FakeResponse(
            {"email": "a@b.test"},
            status=200,
        )

        verify_authenticated_session("http://localhost:8090")

    def test_verify_authenticated_session_sends_me_request_through_zap_proxy(self):
        zap_url = "http://localhost:8090"
        with (
            patch("zap_runtime.urllib.request.ProxyHandler") as proxy_handler,
            patch("zap_runtime.urllib.request.build_opener") as build_opener,
        ):
            build_opener.return_value.open.return_value = FakeResponse(
                {"email": "a@b.test"},
                status=200,
            )

            verify_authenticated_session(zap_url, timeout=11)

        proxy_handler.assert_called_once_with({"http": zap_url, "https": zap_url})
        build_opener.assert_called_once_with(proxy_handler.return_value)
        open_call = build_opener.return_value.open.call_args
        request = open_call.args[0]
        self.assertEqual(request.full_url, "http://localhost:3000/api/users/me")
        self.assertEqual(request.get_method(), "GET")
        self.assertEqual(open_call.kwargs["timeout"], 11)

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

    @patch.dict(os.environ, {"ZAP_IMAGE": "zaproxy/zap-stable:test"}, clear=False)
    @patch("zap_runtime.subprocess.run")
    def test_docker_manager_can_use_image_from_environment(self, run):
        run.return_value.returncode = 0
        manager = ZapDockerManager(port=8090, container_name="test-zap")

        manager.start()

        run.assert_any_call(
            [
                "docker", "run", "--rm", "-d", "--name", "test-zap",
                "--network", "host", "zaproxy/zap-stable:test",
                "zap.sh", "-daemon", "-port", "8090", "-host", "0.0.0.0",
                "-config", "api.disablekey=true",
            ],
            check=True,
            capture_output=True,
            text=True,
        )

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
    def test_docker_manager_raises_when_docker_stop_fails(self, run):
        run.return_value = subprocess.CompletedProcess(
            ["docker", "stop", "test-zap"],
            returncode=1,
            stdout="",
            stderr="stop failed",
        )
        manager = ZapDockerManager(container_name="test-zap")
        manager.started = True

        with self.assertRaisesRegex(RuntimeError, "docker stop failed|stop failed"):
            manager.stop()

        self.assertFalse(manager.started)

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
