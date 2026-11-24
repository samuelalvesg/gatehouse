"""Tests for the translation completeness check. Run: python3 -m unittest discover -s scripts/i18n"""

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_l10n_completeness as cl  # noqa: E402


class L10nTest(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def arb(self, name, data):
        (self.dir / name).write_text(json.dumps(data), encoding="utf-8")

    def test_complete_translation_passes(self):
        self.arb("app_en.arb", {"@@locale": "en", "hello": "Hello", "@hello": {}})
        self.arb("app_pt.arb", {"@@locale": "pt", "hello": "Olá"})
        self.assertEqual(cl.check(self.dir, "app_en.arb", "app_*.arb"), [])

    def test_missing_key_is_reported(self):
        self.arb("app_en.arb", {"hello": "Hello", "bye": "Bye"})
        self.arb("app_pt.arb", {"hello": "Olá"})
        report = cl.check(self.dir, "app_en.arb", "app_*.arb")
        self.assertEqual(report, [("app_pt.arb", ["bye"], [])])

    def test_extra_key_is_reported(self):
        self.arb("app_en.arb", {"hello": "Hello"})
        self.arb("app_pt.arb", {"hello": "Olá", "old": "x"})
        self.assertEqual(cl.check(self.dir, "app_en.arb", "app_*.arb"), [("app_pt.arb", [], ["old"])])

    def test_missing_reference_is_not_verified(self):
        self.assertIsNone(cl.check(self.dir, "app_en.arb", "app_*.arb"))


if __name__ == "__main__":
    unittest.main()
