import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from scan_zap import build_parser


class ScanZapCliTests(unittest.TestCase):
    def test_parser_does_not_accept_scan_mode_argument(self):
        parser = build_parser(load_env=False)

        with self.assertRaises(SystemExit):
            parser.parse_args(["--scan-mode", "basic"])


if __name__ == "__main__":
    unittest.main()
