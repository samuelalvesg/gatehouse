"""Tests for the backlog tools. Run: python3 -m unittest discover -s scripts/backlog"""

import io
import contextlib
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_backlog  # noqa: E402
import new_item  # noqa: E402
import set_status  # noqa: E402
import triage_backlog  # noqa: E402

INDEX = """# Backlog

| ID | Epic | Title | Status | Link |
|---|---|---|---|---|
| `1` | core | Add export | 📝 Registered | [open](backlog/core/add-export.md) |
| `2` | ui | Dark theme | 🟡 Partial | [open](backlog/ui/dark-theme.md) |
"""

ITEM_1 = """# Add export

> **Epic:** `core` · **ID:** `1` · **Status:** 📝 Registered · **Registered:** 2026-01-01

---

- [ ] write the exporter
"""

ITEM_2 = """# Dark theme

> **Epic:** `ui` · **ID:** `2` · **Status:** 🟡 Partial · **Registered:** 2026-01-02

---

- [x] palette
- [ ] contrast check
"""


class BacklogTest(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        (self.root / "docs" / "backlog" / "core").mkdir(parents=True)
        (self.root / "docs" / "backlog" / "ui").mkdir(parents=True)
        (self.root / "docs" / "BACKLOG.md").write_text(INDEX, encoding="utf-8")
        (self.root / "docs" / "backlog" / "core" / "add-export.md").write_text(ITEM_1, encoding="utf-8")
        (self.root / "docs" / "backlog" / "ui" / "dark-theme.md").write_text(ITEM_2, encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def quiet(self, fn, *args):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return fn(*args)

    def read(self, rel):
        return (self.root / rel).read_text(encoding="utf-8")

    def test_clean_backlog_passes_check(self):
        self.assertEqual(check_backlog.run(self.root), [])

    def test_wrong_epic_folder_is_reported(self):
        (self.root / "docs" / "backlog" / "ui" / "add-export.md").write_text(ITEM_1, encoding="utf-8")
        problems = check_backlog.run(self.root)
        self.assertTrue(any(p.startswith("C2") for p in problems))
        self.assertTrue(any(p.startswith("C5") for p in problems))

    def test_done_item_in_index_is_reported(self):
        (self.root / "docs" / "backlog" / "core" / "add-export.md").write_text(
            ITEM_1.replace("📝 Registered", "✅ Done").replace("- [ ] write the exporter", "- [x] write the exporter"),
            encoding="utf-8",
        )
        problems = check_backlog.run(self.root)
        self.assertTrue(any(p.startswith("C6") for p in problems))
        self.assertTrue(any(p.startswith("C7") for p in problems))

    def test_done_with_open_box_is_reported(self):
        (self.root / "docs" / "backlog" / "core" / "add-export.md").write_text(
            ITEM_1.replace("📝 Registered", "✅ Done"), encoding="utf-8"
        )
        self.assertTrue(any(p.startswith("C8") for p in check_backlog.run(self.root)))

    def test_set_status_refuses_done_with_open_boxes(self):
        code = self.quiet(set_status.main, ["add-export", "--status", "✅ Done", "--root", str(self.root)])
        self.assertEqual(code, 1)
        self.assertIn("📝 Registered", self.read("docs/backlog/core/add-export.md"))

    def test_set_status_updates_item_and_index(self):
        self.assertEqual(
            self.quiet(set_status.main, ["add-export", "--status", "🟡 In progress", "--root", str(self.root)]), 0
        )
        self.assertIn("**Status:** 🟡 In progress", self.read("docs/backlog/core/add-export.md"))
        self.assertIn("| 🟡 In progress | [open](backlog/core/add-export.md)", self.read("docs/BACKLOG.md"))
        self.assertEqual(check_backlog.run(self.root), [])

    def test_new_item_creates_file_and_index_row(self):
        code = self.quiet(
            new_item.main,
            ["--root", str(self.root), "--epic", "core", "--title", "Import CSV!", "--id", "3"],
        )
        self.assertEqual(code, 0)
        self.assertTrue((self.root / "docs" / "backlog" / "core" / "import-csv.md").is_file())
        self.assertIn("| `3` | core | Import CSV! |", self.read("docs/BACKLOG.md"))
        self.assertEqual(check_backlog.run(self.root), [])

    def test_new_item_refuses_unknown_status(self):
        code = self.quiet(
            new_item.main,
            ["--root", str(self.root), "--epic", "core", "--title", "X", "--status", "Maybe"],
        )
        self.assertEqual(code, 2)

    def test_triage_flags_are_factual(self):
        rows = {r[0]: r for r in triage_backlog.rows(self.root)}
        self.assertEqual(rows["1"][4], "1")  # open boxes
        self.assertEqual(rows["2"][5], "1")  # done boxes
        self.assertEqual(rows["2"][6], "")


if __name__ == "__main__":
    unittest.main()
