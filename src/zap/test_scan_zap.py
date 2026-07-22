import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.modules.setdefault("zapv2", types.SimpleNamespace(ZAPv2=object))

from scan_zap import build_parser, execute_scan


class ScanZapCliTests(unittest.TestCase):
    def test_parser_does_not_accept_scan_mode_argument(self):
        parser = build_parser(load_env=False)

        with self.assertRaises(SystemExit):
            parser.parse_args(["--scan-mode", "basic"])

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


if __name__ == "__main__":
    unittest.main()
