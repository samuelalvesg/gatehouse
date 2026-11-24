"""Tests for the skill ID checker. Run: python3 -m unittest discover -s scripts/skills"""

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_skill_ids as cs  # noqa: E402


class IdTest(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.skills = self.root / ".agents" / "skills"
        (self.skills / cs.OWNER).mkdir(parents=True)
        (self.skills / cs.OWNER / "SKILL.md").write_text(
            "# Checks\n- **A1** No secrets in public variables.\n- **G4** Hash cap.\n", encoding="utf-8")
        (self.root / "scripts" / "security").mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def scanner(self, ids):
        body = "\n".join(f'spec = {{"{i}": ("x", "HIGH")}}' for i in ids)
        (self.root / "scripts" / "security" / "scan_web_patterns.py").write_text(body + "\n", encoding="utf-8")

    def test_all_scanner_ids_exist(self):
        self.scanner(["A1", "G4"])
        self.assertEqual(cs.integrity(self.root, self.skills), [])

    def test_missing_scanner_id_is_reported(self):
        self.scanner(["A1", "Z9"])
        self.assertEqual(cs.integrity(self.root, self.skills), [f"scanner cites Z9, which {cs.OWNER} does not define"])

    def test_snapshot_then_compare_shows_removal_and_rewording(self):
        before = cs.snapshot(self.skills)
        (self.skills / cs.OWNER / "SKILL.md").write_text("- **A1** Reworded text.\n", encoding="utf-8")
        changes = cs.compare(before, cs.snapshot(self.skills))
        self.assertIn(f"REWORDED {cs.OWNER} A1", changes)
        self.assertIn(f"REMOVED  {cs.OWNER} G4", changes)

    def test_snapshot_round_trips_through_json(self):
        data = json.loads(json.dumps(cs.snapshot(self.skills)))
        self.assertEqual(cs.compare(data, cs.snapshot(self.skills)), [])


if __name__ == "__main__":
    unittest.main()
