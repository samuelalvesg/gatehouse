"""Tests for the scope check. Run: python3 -m unittest discover -s scripts/security"""

import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import scope_check as sc  # noqa: E402

BASE = {
    "owner": "Team A",
    "authorized_by": "CTO",
    "environment": "staging",
    "valid_from": "2026-11-01",
    "valid_until": "2026-11-30",
    "allowed_hosts": ["staging.example.test"],
}
TODAY = date(2026, 11, 15)


class ScopeTest(unittest.TestCase):
    def test_in_scope_target_has_no_reasons(self):
        self.assertEqual(sc.check(BASE, "https://staging.example.test/login", TODAY), [])

    def test_other_host_is_refused(self):
        reasons = sc.check(BASE, "https://other.example.test", TODAY)
        self.assertTrue(any("not in allowed_hosts" in r for r in reasons))

    def test_expired_window_is_refused(self):
        reasons = sc.check(BASE, "staging.example.test", date(2026, 12, 1))
        self.assertIn("outside the authorized period", reasons)

    def test_production_needs_an_explicit_flag(self):
        prod = dict(BASE, environment="production", allowed_hosts=["app.example.test"])
        self.assertIn("production is not authorized", sc.check(prod, "app.example.test", TODAY))
        self.assertEqual(sc.check(dict(prod, allow_production=True), "app.example.test", TODAY), [])

    def test_missing_field_is_invalid(self):
        with self.assertRaises(ValueError):
            sc.check({k: v for k, v in BASE.items() if k != "authorized_by"}, "x", TODAY)


if __name__ == "__main__":
    unittest.main()
