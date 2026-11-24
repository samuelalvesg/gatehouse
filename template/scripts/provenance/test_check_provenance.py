"""Tests for the provenance check. Run: python3 -m unittest discover -s scripts/provenance"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_provenance as cp  # noqa: E402

FULL = """# Provenance

- type: copied, unchanged
- source: https://example.test/repo.git
- license: MIT
- commit: abc1234
- last_checked: 2026-11-24
"""


class ProvenanceTest(unittest.TestCase):
    def write(self, text):
        d = Path(tempfile.mkdtemp())
        p = d / "PROVENANCE.md"
        p.write_text(text, encoding="utf-8")
        return p

    def test_complete_record_is_ok_offline(self):
        self.assertEqual(cp.check(self.write(FULL), online=False), [("OK", "fields recorded")])

    def test_missing_field_is_reported(self):
        text = FULL.replace("- license: MIT\n", "")
        rows = cp.check(self.write(text), online=False)
        self.assertEqual(rows[0][0], "REVIEW")
        self.assertIn("license", rows[0][1])

    def test_unrecorded_commit_is_not_verified(self):
        rows = cp.check(self.write(FULL.replace("abc1234", "NOT VERIFIED")), online=False)
        self.assertEqual(rows[0][0], "NOT VERIFIED")

    def test_not_verified_with_a_note_is_not_verified(self):
        rows = cp.check(self.write(FULL.replace("abc1234", "NOT VERIFIED (not recorded when copied)")), online=False)
        self.assertEqual(rows[0][0], "NOT VERIFIED")

    def test_upstream_moved_is_review(self):
        rows = cp.check(self.write(FULL), online=True, head_of=lambda s: "ffff0000" + "0" * 32)
        self.assertEqual(rows[0][0], "REVIEW")

    def test_upstream_same_commit_is_ok(self):
        rows = cp.check(self.write(FULL), online=True, head_of=lambda s: "abc1234" + "0" * 33)
        self.assertEqual(rows, [("OK", "fields recorded")])

    def test_unreachable_source_is_not_verified(self):
        rows = cp.check(self.write(FULL), online=True, head_of=lambda s: None)
        self.assertEqual(rows[0][0], "NOT VERIFIED")


if __name__ == "__main__":
    unittest.main()
