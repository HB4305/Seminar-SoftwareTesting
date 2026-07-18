import io
import os
import unittest
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))

from scan_zap import (
    OWASP_TOP10_2025_POLICY_NAME,
    build_parser,
    configure_scan_policy,
    execute_scan,
    run,
    write_report,
)


class ScanZapTests(unittest.TestCase):
    def test_parser_defaults_to_managed_anonymous_scan(self):
        args = build_parser(load_env=False).parse_args([])
        self.assertEqual(args.auth_role, "none")
        self.assertFalse(args.external_zap)
        self.assertEqual(
            Path(args.report_file),
            Path(__file__).resolve().parent / "output" / "zap_scan_report.html",
        )

    @patch.dict(
        os.environ,
        {
            "ZAP_TARGET": "http://localhost:5173",
            "ZAP_URL": "http://localhost:9090",
            "ZAP_API_KEY": "dev-key",
            "ZAP_AUTH_ROLE": "user",
            "ZAP_FORCED_USER": "true",
            "ZAP_AJAX_SPIDER": "1",
            "ZAP_EXTERNAL_ZAP": "yes",
            "ZAP_SCAN_MODE": "owasp-top10-2025",
            "ZAP_REPORT_FORMAT": "json",
            "ZAP_REPORT_FILE": "src/zap/output/from-env.json",
        },
        clear=False,
    )
    def test_parser_defaults_can_come_from_environment(self):
        args = build_parser(load_env=False).parse_args([])

        self.assertEqual(args.target, "http://localhost:5173")
        self.assertEqual(args.zap_url, "http://localhost:9090")
        self.assertEqual(args.api_key, "dev-key")
        self.assertEqual(args.auth_role, "user")
        self.assertTrue(args.forced_user)
        self.assertTrue(args.ajax_spider)
        self.assertTrue(args.external_zap)
        self.assertEqual(args.scan_mode, "owasp-top10-2025")
        self.assertEqual(args.report_format, "json")
        self.assertEqual(args.report_file, "src/zap/output/from-env.json")

    @patch.dict(
        os.environ,
        {
            "ZAP_TARGET": "http://localhost:5173",
            "ZAP_AUTH_ROLE": "user",
            "ZAP_FORCED_USER": "true",
            "ZAP_REPORT_FORMAT": "json",
        },
        clear=False,
    )
    def test_cli_flags_override_environment_defaults(self):
        args = build_parser(load_env=False).parse_args(
            [
                "--target",
                "http://localhost:3000",
                "--auth-role",
                "admin",
                "--report-format",
                "html",
            ]
        )

        self.assertEqual(args.target, "http://localhost:3000")
        self.assertEqual(args.auth_role, "admin")
        self.assertTrue(args.forced_user)
        self.assertEqual(args.report_format, "html")

    def test_env_example_documents_zap_configuration(self):
        example = (Path(__file__).resolve().parent / ".env.example").read_text(
            encoding="utf-8"
        )

        for key in (
            "ZAP_TARGET",
            "ZAP_URL",
            "ZAP_AUTH_ROLE",
            "ZAP_FORCED_USER",
            "ZAP_AJAX_SPIDER",
            "ZAP_EXTERNAL_ZAP",
            "ZAP_SCAN_MODE",
            "ZAP_USER_EMAIL",
            "ZAP_USER_PASSWORD",
            "ZAP_ADMIN_EMAIL",
            "ZAP_ADMIN_PASSWORD",
            "OPENROUTER_API_KEY",
            "OPENROUTER_MODEL",
        ):
            with self.subTest(key=key):
                self.assertIn(f"{key}=", example)

    def test_parser_help_shows_default_report_path(self):
        help_text = build_parser(load_env=False).format_help()

        self.assertIn("src/zap/output/zap_scan_report.html", help_text)

    def test_output_file_alias_selects_report_path(self):
        args = build_parser(load_env=False).parse_args(
            ["--output-file", "src/zap/output/frontend_user.html"]
        )

        self.assertEqual(args.report_file, "src/zap/output/frontend_user.html")

    def test_write_report_uses_official_reports_addon_for_html(self):
        zap = MagicMock()
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "report.html"

            write_report(zap, "html", output_path)

        zap.reports.generate.assert_called_once_with(
            title="EShop ZAP Scan Report",
            template="modern",
            reportfilename="report.html",
            reportdir=str(Path(temp_dir)),
            display="false",
        )
        zap.core.htmlreport.assert_not_called()

    def test_write_report_falls_back_to_core_report_when_official_addon_missing(self):
        zap = MagicMock()
        zap.reports.generate.side_effect = RuntimeError("reports add-on missing")
        zap.core.htmlreport.return_value = "<html>fallback</html>"
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "fallback.html"

            write_report(zap, "html", output_path)

            self.assertEqual(
                output_path.resolve().read_text(encoding="utf-8"),
                "<html>fallback</html>",
            )

    def test_configure_scan_policy_keeps_basic_mode_default_policy(self):
        zap = MagicMock()

        self.assertIsNone(configure_scan_policy(zap, "basic"))

        zap.ascan.add_scan_policy.assert_not_called()
        zap.ascan.enable_scanners.assert_not_called()

    def test_configure_scan_policy_creates_owasp_top10_2025_policy_from_alert_tags(self):
        zap = MagicMock()
        zap.ascan.scanners.return_value = [
            {"id": "40012", "name": "Cross Site Scripting", "alertTags": ["OWASP_2025_A03"]},
            {"id": "40018", "name": "SQL Injection", "alertTags": {"OWASP_2025_A03": ""}},
            {"id": "90001", "name": "Unrelated Scanner", "alertTags": ["CUSTOM"]},
        ]

        self.assertEqual(
            configure_scan_policy(zap, "owasp-top10-2025"),
            OWASP_TOP10_2025_POLICY_NAME,
        )

        zap.ascan.add_scan_policy.assert_called_once_with(OWASP_TOP10_2025_POLICY_NAME)
        zap.ascan.disable_scanners.assert_called_once_with(
            "40012,40018,90001",
            scanpolicyname=OWASP_TOP10_2025_POLICY_NAME,
        )
        zap.ascan.enable_scanners.assert_called_once_with(
            "40012,40018",
            scanpolicyname=OWASP_TOP10_2025_POLICY_NAME,
        )

    def test_configure_scan_policy_uses_owasp_top10_2025_id_fallback_without_alert_tags(self):
        zap = MagicMock()
        zap.ascan.scanners.return_value = [
            {"id": "40012", "name": "Cross Site Scripting"},
            {"id": "90001", "name": "Unrelated Scanner"},
        ]

        self.assertEqual(
            configure_scan_policy(zap, "owasp-top10-2025"),
            OWASP_TOP10_2025_POLICY_NAME,
        )

        zap.ascan.disable_scanners.assert_called_once_with(
            "40012,90001",
            scanpolicyname=OWASP_TOP10_2025_POLICY_NAME,
        )
        zap.ascan.enable_scanners.assert_called_once_with(
            "40012",
            scanpolicyname=OWASP_TOP10_2025_POLICY_NAME,
        )

    def test_configure_scan_policy_rejects_owasp_mode_without_matching_scanners(self):
        zap = MagicMock()
        zap.ascan.scanners.return_value = [
            {"id": "90001", "name": "Unrelated Scanner", "alertTags": ["CUSTOM"]},
        ]

        with self.assertRaisesRegex(RuntimeError, "OWASP Top 10 2025"):
            configure_scan_policy(zap, "owasp-top10-2025")

    @patch("scan_zap.wait_for_passive_scan")
    @patch("scan_zap.check_scan_status")
    @patch("scan_zap.time.sleep")
    def test_execute_scan_uses_configured_policy_for_active_scan(
        self, sleep, check_scan_status, wait_for_passive_scan
    ):
        zap = MagicMock()
        zap.spider.scan.return_value = "spider-1"
        zap.ascan.scan.return_value = "active-1"

        execute_scan(
            zap,
            "http://localhost:3000",
            context_id="7",
            ajax_spider=False,
            scan_policy_name=OWASP_TOP10_2025_POLICY_NAME,
        )

        zap.ascan.scan.assert_called_once_with(
            "http://localhost:3000",
            contextid="7",
            scanpolicyname=OWASP_TOP10_2025_POLICY_NAME,
        )

    @patch("scan_zap.ZAPv2")
    @patch("scan_zap.ZapDockerManager")
    @patch("scan_zap.wait_for_zap")
    def test_run_stops_managed_container_on_connection_failure(self, wait_for_zap, manager_cls, zap_cls):
        manager = manager_cls.return_value
        wait_for_zap.side_effect = RuntimeError("not ready")
        args = build_parser(load_env=False).parse_args([])

        self.assertEqual(run(args), 1)
        manager.start.assert_called_once()
        manager.stop.assert_called_once()

    @patch("scan_zap.write_report")
    @patch("scan_zap.execute_scan")
    @patch("scan_zap.verify_authenticated_session")
    @patch("scan_zap.cleanup_authenticated_context")
    @patch("scan_zap.configure_authenticated_context")
    @patch("scan_zap.login_for_token", return_value="jwt-value")
    @patch("scan_zap.get_credential")
    @patch("scan_zap.ensure_context", return_value="7")
    @patch("scan_zap.wait_for_zap", return_value="2.16.1")
    @patch("scan_zap.ZapDockerManager")
    @patch("scan_zap.ZAPv2")
    def test_run_configures_and_cleans_authenticated_scan(
        self,
        zap_cls,
        manager_cls,
        wait_for_zap,
        ensure_context,
        get_credential,
        login_for_token,
        configure_authenticated_context,
        cleanup_authenticated_context,
        verify_authenticated_session,
        execute_scan,
        write_report,
    ):
        credential = MagicMock(email="test@eshop.com", password="secret")
        get_credential.return_value = credential
        configure_authenticated_context.return_value.context_id = "7"
        args = build_parser(load_env=False).parse_args(["--auth-role", "user", "--forced-user"])

        self.assertEqual(run(args), 0)

        login_for_token.assert_called_once_with(args.zap_url, credential)
        configure_authenticated_context.assert_called_once_with(
            zap_cls.return_value, credential, "jwt-value", True
        )
        verify_authenticated_session.assert_called_once_with(args.zap_url)
        execute_scan.assert_called_once_with(
            zap_cls.return_value, args.target, "7", False, None
        )
        cleanup_authenticated_context.assert_called_once_with(zap_cls.return_value, True)
        manager_cls.return_value.stop.assert_called_once()

    @patch("scan_zap.write_report")
    @patch("scan_zap.execute_scan")
    @patch("scan_zap.print_alert_summary")
    @patch("scan_zap.configure_scan_policy", return_value=None)
    @patch("scan_zap.get_credential", return_value=None)
    @patch("scan_zap.ensure_context", return_value="7")
    @patch("scan_zap.wait_for_zap", return_value="2.17.0")
    @patch("scan_zap.ZapDockerManager")
    @patch("scan_zap.ZAPv2")
    def test_run_mounts_report_output_directory_for_managed_zap(
        self,
        zap_cls,
        manager_cls,
        wait_for_zap,
        ensure_context,
        get_credential,
        configure_scan_policy,
        print_alert_summary,
        execute_scan,
        write_report,
    ):
        args = build_parser(load_env=False).parse_args(
            ["--output-file", "tmp/zap/backend_owasp2025.html"]
        )

        self.assertEqual(run(args), 0)

        manager_cls.assert_called_once_with(
            port=8090,
            writable_dir=str((Path.cwd() / "tmp/zap").resolve()),
        )

    @patch("scan_zap.write_report")
    @patch("scan_zap.execute_scan")
    @patch("scan_zap.verify_authenticated_session")
    @patch("scan_zap.cleanup_authenticated_context")
    @patch("scan_zap.configure_authenticated_context")
    @patch("scan_zap.login_for_token", return_value="jwt-value")
    @patch("scan_zap.get_credential")
    @patch("scan_zap.ensure_context", return_value="7")
    @patch("scan_zap.wait_for_zap", return_value="2.16.1")
    @patch("scan_zap.ZapDockerManager")
    @patch("scan_zap.ZAPv2")
    def test_run_returns_one_when_auth_cleanup_fails_after_success(
        self,
        zap_cls,
        manager_cls,
        wait_for_zap,
        ensure_context,
        get_credential,
        login_for_token,
        configure_authenticated_context,
        cleanup_authenticated_context,
        verify_authenticated_session,
        execute_scan,
        write_report,
    ):
        credential = MagicMock(email="test@eshop.com", password="secret")
        get_credential.return_value = credential
        configure_authenticated_context.return_value.context_id = "7"
        cleanup_authenticated_context.side_effect = RuntimeError("cleanup failed")
        args = build_parser(load_env=False).parse_args(["--auth-role", "user", "--forced-user"])

        with patch("sys.stderr", new_callable=io.StringIO) as stderr:
            self.assertEqual(run(args), 1)

        cleanup_authenticated_context.assert_called_once_with(zap_cls.return_value, True)
        manager_cls.return_value.stop.assert_called_once()
        self.assertIn("cleanup failed", stderr.getvalue())

    @patch("scan_zap.write_report")
    @patch("scan_zap.execute_scan")
    @patch("scan_zap.get_credential", return_value=None)
    @patch("scan_zap.ensure_context", return_value="7")
    @patch("scan_zap.wait_for_zap", return_value="2.16.1")
    @patch("scan_zap.ZapDockerManager")
    @patch("scan_zap.ZAPv2")
    def test_run_returns_one_when_manager_stop_fails_after_success(
        self,
        zap_cls,
        manager_cls,
        wait_for_zap,
        ensure_context,
        get_credential,
        execute_scan,
        write_report,
    ):
        manager_cls.return_value.stop.side_effect = RuntimeError("stop failed")
        args = build_parser(load_env=False).parse_args([])

        with patch("sys.stderr", new_callable=io.StringIO) as stderr:
            self.assertEqual(run(args), 1)

        manager_cls.return_value.stop.assert_called_once()
        self.assertIn("stop failed", stderr.getvalue())

    @patch("scan_zap.ZAPv2")
    @patch("scan_zap.ZapDockerManager")
    def test_run_returns_one_for_malformed_managed_zap_url_without_starting_docker(
        self, manager_cls, zap_cls
    ):
        args = build_parser(load_env=False).parse_args(["--zap-url", "http://localhost:abc"])

        with patch("sys.stderr", new_callable=io.StringIO):
            self.assertEqual(run(args), 1)

        manager_cls.assert_not_called()
        zap_cls.assert_not_called()

    @patch("scan_zap.ZAPv2")
    @patch("scan_zap.ZapDockerManager")
    def test_run_rejects_authenticated_scan_through_remote_zap_url(
        self, manager_cls, zap_cls
    ):
        args = build_parser(load_env=False).parse_args(
            ["--auth-role", "user", "--zap-url", "http://evil.example:8090"]
        )

        with patch("sys.stderr", new_callable=io.StringIO):
            self.assertEqual(run(args), 1)

        manager_cls.assert_not_called()
        zap_cls.assert_not_called()

    @patch("scan_zap.ZAPv2")
    @patch("scan_zap.ZapDockerManager")
    def test_run_rejects_authenticated_scan_with_malformed_zap_url_port(
        self, manager_cls, zap_cls
    ):
        args = build_parser(load_env=False).parse_args(
            ["--auth-role", "user", "--external-zap", "--zap-url", "http://localhost:abc"]
        )

        with patch("sys.stderr", new_callable=io.StringIO):
            self.assertEqual(run(args), 1)

        manager_cls.assert_not_called()
        zap_cls.assert_not_called()
