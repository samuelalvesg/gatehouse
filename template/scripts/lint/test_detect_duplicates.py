"""Tests for detect_duplicates. Run: python3 -m unittest discover -s scripts/lint"""

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import detect_duplicates as dd  # noqa: E402

BLOCK = "x = load()\ny = parse(x)\nz = check(y)\nw = save(z)\nlog(w)\nreturn w\nclean()\ndone()\n"


class DuplicatesTest(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def test_block_in_two_files_is_found(self):
        (self.root / "a.py").write_text("# header\n" + BLOCK, encoding="utf-8")
        (self.root / "b.py").write_text(BLOCK, encoding="utf-8")
        self.assertTrue(dd.duplicates(self.root, 8, {".py"}))

    def test_unique_code_is_not_reported(self):
        (self.root / "a.py").write_text(BLOCK, encoding="utf-8")
        (self.root / "b.py").write_text(BLOCK.replace("load", "fetch"), encoding="utf-8")
        self.assertEqual(dd.duplicates(self.root, 8, {".py"}), [])

    def test_repeat_inside_one_file_is_not_reported(self):
        (self.root / "a.py").write_text(BLOCK + BLOCK, encoding="utf-8")
        self.assertEqual(dd.duplicates(self.root, 8, {".py"}), [])


if __name__ == "__main__":
    unittest.main()
