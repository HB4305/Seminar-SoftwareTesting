import io
import unittest
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))

from scan_zap import build_parser, run


class ScanZapTests(unittest.TestCase):
    def test_parser_defaults_to_managed_anonymous_scan(self):
        args = build_parser().parse_args([])
        self.assertEqual(args.auth_role, "none")
        self.assertFalse(args.external_zap)
        self.assertEqual(
            Path(args.report_file),
            Path(__file__).resolve().parent / "output" / "zap_scan_report.html",
        )

    @patch("scan_zap.ZAPv2")
    @patch("scan_zap.ZapDockerManager")
    @patch("scan_zap.wait_for_zap")
    def test_run_stops_managed_container_on_connection_failure(self, wait_for_zap, manager_cls, zap_cls):
        manager = manager_cls.return_value
        wait_for_zap.side_effect = RuntimeError("not ready")
        args = build_parser().parse_args([])

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
        args = build_parser().parse_args(["--auth-role", "user", "--forced-user"])

        self.assertEqual(run(args), 0)

        login_for_token.assert_called_once_with(args.zap_url, credential)
        configure_authenticated_context.assert_called_once_with(
            zap_cls.return_value, credential, "jwt-value", True
        )
        verify_authenticated_session.assert_called_once_with(args.zap_url)
        execute_scan.assert_called_once_with(
            zap_cls.return_value, args.target, "7", False
        )
        cleanup_authenticated_context.assert_called_once_with(zap_cls.return_value, True)
        manager_cls.return_value.stop.assert_called_once()

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
        args = build_parser().parse_args(["--auth-role", "user", "--forced-user"])

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
        args = build_parser().parse_args([])

        with patch("sys.stderr", new_callable=io.StringIO) as stderr:
            self.assertEqual(run(args), 1)

        manager_cls.return_value.stop.assert_called_once()
        self.assertIn("stop failed", stderr.getvalue())

    @patch("scan_zap.ZAPv2")
    @patch("scan_zap.ZapDockerManager")
    def test_run_returns_one_for_malformed_managed_zap_url_without_starting_docker(
        self, manager_cls, zap_cls
    ):
        args = build_parser().parse_args(["--zap-url", "http://localhost:abc"])

        with patch("sys.stderr", new_callable=io.StringIO):
            self.assertEqual(run(args), 1)

        manager_cls.assert_not_called()
        zap_cls.assert_not_called()
