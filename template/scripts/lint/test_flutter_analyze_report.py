"""Tests for the analyze parser and the report. Run: python3 -m unittest discover -s scripts/lint"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import flutter_analyze_report as fr  # noqa: E402

SAMPLE = """Analyzing app...

   info • 'Radio' is deprecated and shouldn't be used • lib/home.dart:12:5 • deprecated_member_use
 warning • Unused import: 'dart:io' • lib/io.dart:1:8 • unused_import
   error • Undefined name 'x' • lib/x.dart:4:3 • undefined_identifier

3 issues found. (ran in 1.2s)
"""


class FlutterAnalyzeTest(unittest.TestCase):
    def test_parses_each_issue_line(self):
        issues = fr.parse_analyze(SAMPLE)
        self.assertEqual(len(issues), 3)
        self.assertEqual(issues[0]["rule"], "deprecated_member_use")
        self.assertEqual((issues[0]["file"], issues[0]["line"], issues[0]["col"]), ("lib/home.dart", 12, 5))
        self.assertEqual(issues[1]["severity"], "warning")

    def test_summary_and_rule_filter(self):
        issues = fr.parse_analyze(SAMPLE)
        report = fr.render({"app": issues}, None)
        self.assertIn("| `deprecated_member_use` | 1 |", report)
        filtered = fr.render({"app": issues}, "unused_import")
        self.assertIn("Unused import", filtered)
        self.assertNotIn("Undefined name", filtered)

    def test_empty_output_has_no_issues(self):
        self.assertEqual(fr.parse_analyze("No issues found!\n"), [])


if __name__ == "__main__":
    unittest.main()
