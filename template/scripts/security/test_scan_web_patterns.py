"""Tests for the web pattern scanner. Run: python3 -m unittest discover -s scripts/security"""

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import scan_web_patterns as scan  # noqa: E402


def status(rows, check_id):
    return next(r[2] for r in rows if r[0] == check_id)


class ScanTest(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def put(self, rel, text):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")

    def test_no_source_is_not_verified(self):
        self.assertIsNone(scan.scan(self.root))

    def test_clean_project_passes_the_patterns(self):
        self.put(".gitignore", ".env\n")
        self.put("src/app.ts", "export const x = 1;\n")
        rows = scan.scan(self.root)
        self.assertEqual(status(rows, "A2"), "PASS")
        self.assertEqual(status(rows, "A1"), "PASS")
        self.assertTrue(all(r[2] in {"PASS", "FAIL"} for r in rows))

    def test_public_secret_and_raw_sql_fail(self):
        self.put(".gitignore", ".env\n")
        self.put("src/config.ts", "const k = process.env.NEXT_PUBLIC_SERVICE_ROLE_KEY;\n")
        self.put("src/db.ts", 'db.query(`SELECT * FROM t WHERE id = ${id}`);\n')
        rows = scan.scan(self.root)
        self.assertEqual(status(rows, "A1"), "FAIL")
        self.assertEqual(status(rows, "H3"), "FAIL")

    def test_webhook_needs_a_signature_check(self):
        self.put("api/webhook/route.ts", "export async function POST(req) { return ok(); }\n")
        self.assertEqual(status(scan.scan(self.root), "E3"), "FAIL")
        self.put("api/webhook/route.ts", "export async function POST(req) { verify(req); }\n")
        self.assertEqual(status(scan.scan(self.root), "E3"), "PASS")

    def test_unsafe_html_passes_when_sanitized(self):
        self.put("ui/a.tsx", "<div dangerouslySetInnerHTML={{__html: x}} />\n")
        self.assertEqual(status(scan.scan(self.root), "H2"), "FAIL")
        self.put("ui/a.tsx", "import DOMPurify from 'dompurify';\n<div dangerouslySetInnerHTML={{__html: DOMPurify.sanitize(x)}} />\n")
        self.assertEqual(status(scan.scan(self.root), "H2"), "PASS")

    def test_jwt_decode_without_verify_fails(self):
        self.put("auth/token.ts", "const claims = jwt.decode(token);\n")
        self.assertEqual(status(scan.scan(self.root), "J1"), "FAIL")
        self.put("auth/token.ts", "const claims = jwt.verify(token, key);\n")
        self.assertEqual(status(scan.scan(self.root), "J1"), "PASS")

    def test_outbound_request_from_input_is_flagged(self):
        self.put("api/proxy.ts", "const r = await fetch(req.query.url);\n")
        self.assertEqual(status(scan.scan(self.root), "I1"), "FAIL")

    def test_cookie_without_httponly_fails(self):
        self.put("auth/session.ts", "res.cookie('s', token, { secure: true });\n")
        self.assertEqual(status(scan.scan(self.root), "F2"), "FAIL")


if __name__ == "__main__":
    unittest.main()
