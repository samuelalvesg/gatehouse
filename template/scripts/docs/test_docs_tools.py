"""Tests for the docs gate and the dependency generator. Run: python3 -m unittest discover -s scripts/docs"""

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "generators"))

import check_docs_fresh  # noqa: E402
import dependencies  # noqa: E402

PUBSPEC_APP = "name: app\ndependencies:\n  core:\n    path: ../core\n"
PUBSPEC_CORE = "name: core\n"


class DocsToolsTest(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        (self.root / "app").mkdir()
        (self.root / "core").mkdir()
        (self.root / "app" / "pubspec.yaml").write_text(PUBSPEC_APP, encoding="utf-8")
        (self.root / "core" / "pubspec.yaml").write_text(PUBSPEC_CORE, encoding="utf-8")
        (self.root / "docs").mkdir()

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def write_generator(self, folder: Path, body: str):
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "gen.py").write_text(body, encoding="utf-8")

    def test_dependencies_graph_has_the_local_edge(self):
        text = dependencies.generate(self.root)
        self.assertIn("app --> core", text)
        self.assertTrue(text.startswith("<!-- GENERATED"))

    def test_no_manifest_means_not_verified(self):
        empty = Path(tempfile.mkdtemp())
        try:
            with self.assertRaises(FileNotFoundError):
                dependencies.generate(empty)
        finally:
            shutil.rmtree(empty, ignore_errors=True)

    def test_missing_generated_file_is_a_violation(self):
        gens = self.root / "gens"
        self.write_generator(gens, 'OUTPUT = "docs/g.md"\ndef generate(root):\n    return "GENERATED\\n"\n')
        bad, missing = check_docs_fresh.check(self.root, gens)
        self.assertTrue(any(b.startswith("G1") and "missing" in b for b in bad))

    def test_stale_and_unmarked_outputs_are_violations(self):
        gens = self.root / "gens"
        self.write_generator(gens, 'OUTPUT = "docs/g.md"\ndef generate(root):\n    return "GENERATED\\nnew\\n"\n')
        (self.root / "docs" / "g.md").write_text("GENERATED\nold\n", encoding="utf-8")
        bad, _ = check_docs_fresh.check(self.root, gens)
        self.assertTrue(any("out of date" in b for b in bad))
        (self.root / "docs" / "g.md").write_text("plain\n", encoding="utf-8")
        bad, _ = check_docs_fresh.check(self.root, gens)
        self.assertTrue(any(b.startswith("G3") for b in bad))

    def test_rules_flag_stale_statements_unless_ignored(self):
        (self.root / "docs" / "freshness.json").write_text(
            '{"canonical": ["README.md"], "rules": [{"id": "R1", "pattern": "\\\\b\\\\d+ tests\\\\b", "message": "typed count"}]}',
            encoding="utf-8",
        )
        (self.root / "README.md").write_text("We have 40 tests.\nOld: 12 tests. docs-fresh: ignore\n", encoding="utf-8")
        bad, _ = check_docs_fresh.check(self.root, HERE / "nothing")
        self.assertEqual([b for b in bad if b.startswith("G2")], ["G2/R1 README.md:1: typed count"])


if __name__ == "__main__":
    unittest.main()
