import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.modules.setdefault("zapv2", types.SimpleNamespace(ZAPv2=object))

from scan_zap import build_parser, configure_scan_policy, execute_scan


class ScanZapCliTests(unittest.TestCase):
    def test_parser_accepts_scan_mode_argument(self):
        parser = build_parser(load_env=False)

        args = parser.parse_args(["--scan-mode", "owasp-top10-2025"])

        self.assertEqual(args.scan_mode, "owasp-top10-2025")

    def test_parser_accepts_max_urls(self):
        parser = build_parser(load_env=False)

        args = parser.parse_args(["--max-urls", "250"])

        self.assertEqual(args.max_urls, 250)

    def test_parser_rejects_non_positive_max_urls(self):
        parser = build_parser(load_env=False)

        with self.assertRaises(SystemExit):
            parser.parse_args(["--max-urls", "0"])


class _FakeSpider:
    def __init__(self):
        self.scan_called = False

    def scan(self, target, contextname=None):
        self.scan_called = True
        return "spider-1"

    def status(self, scan_id):
        return "100"


class _FakeAjaxSpider:
    status = "stopped"


class _FakePassiveScan:
    records_to_scan = "0"


class _FakeActiveScan:
    def __init__(self):
        self.scan_called = False

    def scan(self, *args, **kwargs):
        self.scan_called = True
        return "active-1"

    def status(self, scan_id):
        return "100"


class _FakePolicyAscan:
    def __init__(self, scanners):
        self._scanners = scanners
        self.removed_policy = None
        self.added_policy = None
        self.disabled_ids = None
        self.enabled_ids = None
        self.disabled_policy = None
        self.enabled_policy = None

    def scanners(self):
        return self._scanners

    def remove_scan_policy(self, scanpolicyname):
        self.removed_policy = scanpolicyname

    def add_scan_policy(self, scanpolicyname):
        self.added_policy = scanpolicyname

    def disable_scanners(self, ids, scanpolicyname=None):
        self.disabled_ids = ids
        self.disabled_policy = scanpolicyname

    def enable_scanners(self, ids, scanpolicyname=None):
        self.enabled_ids = ids
        self.enabled_policy = scanpolicyname


class _FakePolicyZap:
    def __init__(self, scanners):
        self.ascan = _FakePolicyAscan(scanners)


class _FakeCore:
    def __init__(self, urls):
        self._urls = urls

    def urls(self, baseurl=None):
        return self._urls


class _FakeZap:
    def __init__(self, urls):
        self.spider = _FakeSpider()
        self.ajaxSpider = _FakeAjaxSpider()
        self.pscan = _FakePassiveScan()
        self.ascan = _FakeActiveScan()
        self.core = _FakeCore(urls)

    def urlopen(self, target):
        return None


class ScanZapMaxUrlsTests(unittest.TestCase):
    def test_execute_scan_skips_active_scan_when_url_budget_is_exceeded(self):
        zap = _FakeZap(
            [
                "http://localhost:5173/",
                "http://localhost:5173/products",
                "http://localhost:5173/cart",
            ]
        )

        with patch("scan_zap.time.sleep", return_value=None):
            execute_scan(
                zap,
                "http://localhost:5173",
                context_id="1",
                ajax_spider=False,
                max_urls=2,
            )

        self.assertTrue(zap.spider.scan_called)
        self.assertFalse(zap.ascan.scan_called)


class ScanZapPolicyTests(unittest.TestCase):
    def test_configure_scan_policy_enables_only_owasp_2025_tagged_scanners(self):
        zap = _FakePolicyZap(
            [
                {"id": "10020", "name": "X-Frame-Options Header", "alertTags": ["OWASP_2025_A02"]},
                {"id": "40044", "name": "External Redirect", "tags": "OWASP_2025_A10"},
                {"id": "99999", "name": "Noise", "alertTags": ["OTHER_TAG"]},
            ]
        )

        policy_name = configure_scan_policy(zap, "owasp-top10-2025")

        self.assertEqual(policy_name, "owasp-top10-2025")
        self.assertEqual(zap.ascan.removed_policy, "owasp-top10-2025")
        self.assertEqual(zap.ascan.added_policy, "owasp-top10-2025")
        self.assertEqual(zap.ascan.disabled_ids, "10020,40044,99999")
        self.assertEqual(zap.ascan.disabled_policy, "owasp-top10-2025")
        self.assertEqual(zap.ascan.enabled_ids, "10020,40044")
        self.assertEqual(zap.ascan.enabled_policy, "owasp-top10-2025")

    def test_configure_scan_policy_falls_back_to_known_owasp_2025_scanner_ids(self):
        zap = _FakePolicyZap(
            [
                {"id": "40014-1", "name": "Cross Site Scripting Persistent"},
                {"id": "40044", "name": "External Redirect"},
                {"id": "99999", "name": "Noise"},
            ]
        )

        policy_name = configure_scan_policy(zap, "owasp-top10-2025")

        self.assertEqual(policy_name, "owasp-top10-2025")
        self.assertEqual(zap.ascan.disabled_ids, "40014,40044,99999")
        self.assertEqual(zap.ascan.enabled_ids, "40014,40044")

    def test_configure_scan_policy_keeps_basic_mode_without_api_calls(self):
        zap = _FakePolicyZap([])

        policy_name = configure_scan_policy(zap, "basic")

        self.assertIsNone(policy_name)
        self.assertIsNone(zap.ascan.removed_policy)
        self.assertIsNone(zap.ascan.added_policy)
        self.assertIsNone(zap.ascan.disabled_ids)
        self.assertIsNone(zap.ascan.enabled_ids)


if __name__ == "__main__":
    unittest.main()
