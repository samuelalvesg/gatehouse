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

    def test_webhook_without_signature_check_is_flagged_for_review(self):
        self.put("api/webhook/route.ts", "app.post('/webhook', (req) => ok());\n")
        self.assertEqual(status(scan.scan(self.root), "E3"), "NOT VERIFIED")
        self.put("api/webhook/route.ts", "app.post('/webhook', (req) => { verify(req); });\n")
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

    def test_login_route_without_rate_limit_is_flagged(self):
        self.put("controllers/AuthController.cs", '[HttpPost("login")]\npublic Task Login() { }\n')
        self.assertEqual(status(scan.scan(self.root), "G1"), "FAIL")
        self.put("controllers/AuthController.cs", '[EnableRateLimiting("Login")]\n[HttpPost("login")]\npublic Task Login() { }\n')
        self.assertEqual(status(scan.scan(self.root), "G1"), "PASS")

    def test_hashing_without_concurrency_cap_is_flagged(self):
        self.put("auth/hasher.cs", "var h = new Argon2id(bytes).GetBytes(32);\n")
        self.assertEqual(status(scan.scan(self.root), "G4"), "FAIL")
        self.put("auth/hasher.cs", "var gate = new SemaphoreSlim(4);\nvar h = new Argon2id(bytes).GetBytes(32);\n")
        self.assertEqual(status(scan.scan(self.root), "G4"), "PASS")

    def test_client_ip_header_without_trust_check_is_flagged(self):
        self.put("net/ip.cs", "var ip = ctx.Request.Headers[\"CF-Connecting-IP\"];\n")
        self.assertEqual(status(scan.scan(self.root), "G8"), "FAIL")
        self.put("net/ip.cs", "opts.KnownProxies.Clear();\n")
        self.assertEqual(status(scan.scan(self.root), "G8"), "FAIL")

    def test_worktree_and_scratch_copies_are_not_scanned(self):
        self.put(".claude/worktrees/x/auth/login.ts", "fetch(req.query.url)\n")
        self.put("scratch/tmp.cs", "var h = new Argon2id(b).GetBytes(32);\n")
        self.put("src/app.ts", "export const ok = true;\n")
        rows = scan.scan(self.root)
        self.assertEqual(status(rows, "G4"), "PASS")
        self.assertEqual(status(rows, "I1"), "PASS")

    def test_comment_mentioning_an_attack_is_not_code(self):
        self.put("net/ip.cs", "// reads CF-Connecting-IP only from trusted edges\n")
        self.assertEqual(status(scan.scan(self.root), "G8"), "PASS")

    def test_test_files_are_not_scanned(self):
        self.put("tests/ip.test.ts", "const ip = req.headers['CF-Connecting-IP'];\n")
        self.put("src/app.ts", "export const ok = true;\n")
        self.assertEqual(status(scan.scan(self.root), "G8"), "PASS")

    def test_validator_is_not_a_login_route(self):
        self.put("validators/LoginRequestValidator.cs", "RuleFor(x => x.Password).MinimumLength(6);\n")
        self.assertEqual(status(scan.scan(self.root), "G1"), "PASS")

    def test_hashing_registration_is_not_a_hash_call(self):
        self.put("di/Services.cs", "services.AddScoped<IPasswordHasher, Argon2PasswordHasher>();\n")
        self.assertEqual(status(scan.scan(self.root), "G4"), "PASS")

    def test_webhook_check_is_review_only(self):
        self.put("api/WebhookController.cs", '[HttpPost("webhook")]\npublic Task Receive() { }\n')
        self.assertEqual(status(scan.scan(self.root), "E3"), "NOT VERIFIED")

    def test_non_login_auth_controller_is_not_flagged(self):
        self.put("controllers/ApiTokensController.cs", '[HttpPost("tokens")]\npublic Task Create() { }\n')
        self.assertEqual(status(scan.scan(self.root), "G1"), "PASS")

    def test_client_ip_read_after_a_trust_check_is_not_flagged(self):
        self.put("net/ip.cs", "if (IsFromTrustedEdge(ctx)) return ctx.Request.Headers[\"CF-Connecting-IP\"];\n")
        self.assertEqual(status(scan.scan(self.root), "G8"), "PASS")

    def test_cap_in_the_hasher_covers_call_sites(self):
        self.put("auth/Argon2PasswordHasher.cs", "var gate = new SemaphoreSlim(4);\nvar h = new Argon2id(b).GetBytes(32);\n")
        self.put("auth/AuthService.cs", "_passwordHasher.VerifyPassword(p, h);\n")
        self.assertEqual(status(scan.scan(self.root), "G4"), "PASS")

    def test_cookie_without_httponly_fails(self):
        self.put("auth/session.ts", "res.cookie('s', token, { secure: true });\n")
        self.assertEqual(status(scan.scan(self.root), "F2"), "FAIL")


if __name__ == "__main__":
    unittest.main()
