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
import check_doc_paths  # noqa: E402
import report_done  # noqa: E402
import split_backlog  # noqa: E402
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

    def test_report_done_lists_only_done_items(self):
        (self.root / "docs" / "backlog" / "ui" / "dark-theme.md").write_text(
            ITEM_2.replace("🟡 Partial", "✅ Done").replace("- [ ] contrast check", "- [x] contrast check"),
            encoding="utf-8",
        )
        self.assertEqual(self.quiet(report_done.main, ["--root", str(self.root)]), 0)
        report = self.read("docs/DONE.md")
        self.assertIn("# Done (1)", report)
        self.assertIn("Dark theme", report)
        self.assertNotIn("Add export", report)

    def test_split_dry_run_writes_nothing(self):
        source = self.root / "old.md"
        source.write_text("Intro line\n\n## First\n\n- [ ] a\n\n## Second\n\nSome text\n", encoding="utf-8")
        (self.root / "docs" / "BACKLOG.md").unlink()
        code = self.quiet(split_backlog.main, ["--root", str(self.root), "--source", str(source), "--epic", "misc"])
        self.assertEqual(code, 0)
        self.assertFalse((self.root / "docs" / "BACKLOG.md").exists())

    def test_split_write_keeps_every_line(self):
        source = self.root / "old.md"
        source.write_text("Intro line\n\n## First\n\n- [ ] a\n\n## Second\n\nSome text\n", encoding="utf-8")
        (self.root / "docs" / "BACKLOG.md").unlink()
        shutil.rmtree(self.root / "docs" / "backlog")
        code = self.quiet(
            split_backlog.main,
            ["--root", str(self.root), "--source", str(source), "--epic", "misc", "--write"],
        )
        self.assertEqual(code, 0)
        self.assertIn("Intro line", self.read("docs/BACKLOG.md"))
        self.assertIn("- [ ] a", self.read("docs/backlog/misc/first.md"))
        self.assertIn("Some text", self.read("docs/backlog/misc/second.md"))
        self.assertEqual(check_backlog.run(self.root), [])

    def test_doc_paths_reports_broken_links_and_ticks(self):
        (self.root / "docs" / "guide.md").write_text(
            "[ok](backlog/ui/dark-theme.md) [bad](missing.md) `docs/nope.md` `docs/BACKLOG.md`\n",
            encoding="utf-8",
        )
        problems = [p for md in check_doc_paths.markdown_files(self.root) for p in check_doc_paths.broken_in(self.root, md)]
        self.assertIn("link -> missing.md", problems)
        self.assertIn("path `docs/nope.md`", problems)
        self.assertNotIn("link -> backlog/ui/dark-theme.md", problems)

    def test_triage_flags_are_factual(self):
        rows = {r[0]: r for r in triage_backlog.rows(self.root)}
        self.assertEqual(rows["1"][4], "1")  # open boxes
        self.assertEqual(rows["2"][5], "1")  # done boxes
        self.assertEqual(rows["2"][6], "")


if __name__ == "__main__":
    unittest.main()
