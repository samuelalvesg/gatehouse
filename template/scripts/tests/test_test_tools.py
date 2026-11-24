"""Tests for repeat_test and check_skipped. Run: python3 -m unittest discover -s scripts/tests"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_skipped as cs  # noqa: E402
import repeat_test as rt  # noqa: E402


class RepeatTest(unittest.TestCase):
    def test_always_passing(self):
        self.assertEqual(rt.main(["--runs", "3", "--", sys.executable, "-c", "import sys; sys.exit(0)"]), 0)

    def test_always_failing(self):
        self.assertEqual(rt.main(["--runs", "2", "--", sys.executable, "-c", "import sys; sys.exit(1)"]), 1)

    def test_flaky_alternates(self):
        counter = Path(tempfile.mkdtemp()) / "n"
        code = ("import pathlib,sys; p=pathlib.Path(sys.argv[1]); "
                "n=int(p.read_text()) if p.exists() else 0; p.write_text(str(n+1)); sys.exit(n%2)")
        self.assertEqual(rt.main(["--runs", "4", "--", sys.executable, "-c", code, str(counter)]), 1)


class SkippedTest(unittest.TestCase):
    def test_dotnet_portuguese_summary_with_no_skips(self):
        self.assertEqual(cs.skipped_count("Aprovado!  – Com falha: 0, Aprovado: 8, Ignorado: 0"), 0)

    def test_dotnet_summary_with_skips_is_counted(self):
        self.assertEqual(cs.skipped_count("Com falha: 0, Aprovado: 8, Ignorado: 3"), 3)

    def test_pytest_summary(self):
        self.assertEqual(cs.skipped_count("=== 5 passed, 2 skipped in 1.20s ==="), 2)

    def test_no_summary_is_not_verified(self):
        self.assertIsNone(cs.skipped_count("compiling...\nnothing else"))


if __name__ == "__main__":
    unittest.main()
