#!/usr/bin/env python3
"""Mechanical pass of the web-app security audit. Standard library only.

It finds the items a pattern can find, and nothing more. Every hit is a lead,
not a verdict: read the file before you mark an item FAIL (see the
web-app-security-audit skill).

Usage:
  python3 scripts/security/scan_web_patterns.py [--root .]

Exit: 0 no FAIL, 1 at least one FAIL, 2 no source files found (not verified).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SKIP = {".git", "node_modules", "build", ".next", "dist", "target", ".dart_tool", "vendor"}
SOURCE = {".ts", ".tsx", ".js", ".jsx", ".mjs", ".py", ".go", ".dart", ".sql", ".php", ".rb", ".cs", ".java", ".kt"}
RE_PUBLIC_SECRET = re.compile(r"(NEXT_PUBLIC_|VITE_|REACT_APP_)\w*(SECRET|PRIVATE|SERVICE_ROLE|PASSWORD|TOKEN)")
RE_SERVICE_KEY = re.compile(r"service[_-]?role", re.I)
RE_UNSAFE_HTML = re.compile(r"dangerouslySetInnerHTML|innerHTML|v-html")
RE_SANITIZER = re.compile(r"DOMPurify|sanitize", re.I)
RE_WEBHOOK = re.compile(r"webhook", re.I)
RE_SIGNATURE = re.compile(r"signature|hmac|constructEvent|verify", re.I)
RE_CORS_STAR = re.compile(r"Access-Control-Allow-Origin[\"']?\s*[:,]\s*[\"']\*")
RE_CREDENTIALS = re.compile(r"Allow-Credentials[\"']?\s*[:,]\s*(true|\"true\")", re.I)
RE_COOKIE_SET = re.compile(r"\b(setCookie|res\.cookie|cookies\(\)\.set|set-cookie)\b", re.I)
RE_COOKIE_FLAGS = re.compile(r"httpOnly", re.I)
RE_AUTH_ROUTE = re.compile(r"(login|signin|sign-in|signup|sign-up|register|reset|forgot|password|auth)", re.I)
RE_LOGIN_ROUTE = re.compile(r"[\"\x27/](login|signin|sign-in)[\"\x27/]", re.I)
RE_HASH_CALL = re.compile(r"HashPassword|VerifyPassword|Argon2id|bcrypt|scrypt", re.I)
RE_CLIENT_IP_HEADER = re.compile(r"CF-Connecting-IP|X-Forwarded-For|X-Real-IP", re.I)
RE_FWD_CLEAR = re.compile(r"KnownProxies\.Clear|KnownIPNetworks\.Clear|KnownNetworks\.Clear")
RE_CONCURRENCY_CAP = re.compile(r"SemaphoreSlim|Semaphore\(|Limiter|Concurrency|WorkerPool", re.I)
RE_RATE_LIMIT = re.compile(r"rate[_-]?limit|throttle", re.I)
RE_RAW_SQL = re.compile(r"(query|execute|raw)\s*\(\s*[`\"'][^`\"']*(\$\{|\"\s*\+|'\s*\+)")
RE_LOCAL_REDIRECT = re.compile(r"callbackUrl|redirectTo|[\"']next[\"']", re.I)
RE_DEBUG_ROUTE = re.compile(r"/(admin|dev|debug|test)(/|$)")
RE_JWT_DECODE = re.compile(r"jwt\.decode\(|decode\(\s*token", re.I)
RE_JWT_VERIFY = re.compile(r"jwt\.verify\(|verifyJwt|jwtVerify|verify\(", re.I)
RE_SECRET_LOG = re.compile(r"console\.(log|info|warn|error)\(.*(password|token|secret)", re.I)
RE_STACK_TO_CLIENT = re.compile(r"(json|send|response|Response)\w*\(.*\.stack\b")
RE_SSRF = re.compile(r"(fetch|axios\.\w+|requests\.\w+|http\.get)\(\s*[`\"']?\s*\$?\{?\s*(req\.|request\.|searchParams|params\.|query\.)", re.I)


def sources(root: Path):
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        parts = p.relative_to(root).parts
        if set(parts[:-1]) & SKIP:
            continue
        if p.suffix in SOURCE or p.name.startswith(".env") or p.name == ".gitignore":
            yield p


def first_line(text: str, rx: re.Pattern) -> int | None:
    m = rx.search(text)
    return text.count("\n", 0, m.start()) + 1 if m else None


def scan(root: Path):
    files = list(sources(root))
    if not any(p.suffix in SOURCE for p in files):
        return None
    rows = []
    ignore = root / ".gitignore"
    gi = ignore.read_text(encoding="utf-8") if ignore.is_file() else ""
    rows.append(("A2", ".env git-ignored", "PASS" if re.search(r"^\.env", gi, re.M) else "FAIL", "HIGH", ".gitignore"))

    hits = {k: [] for k in ("A1", "B1", "D2", "E1", "E3", "E4", "F2", "G1", "H2", "H3", "H4", "I1", "J1", "J6", "M1", "G4", "G8")}
    for p in files:
        if p.suffix not in SOURCE:
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        rel = p.relative_to(root).as_posix()
        if RE_PUBLIC_SECRET.search(text):
            hits["A1"].append(f"{rel}:{first_line(text, RE_PUBLIC_SECRET)}")
        if RE_SERVICE_KEY.search(text) and "server" not in rel.lower() and "migration" not in rel.lower():
            hits["B1"].append(f"{rel}:{first_line(text, RE_SERVICE_KEY)}")
        if RE_UNSAFE_HTML.search(text) and not RE_SANITIZER.search(text):
            hits["H2"].append(f"{rel}:{first_line(text, RE_UNSAFE_HTML)}")
        if RE_DEBUG_ROUTE.search(rel):
            hits["E1"].append(rel)
        if RE_WEBHOOK.search(rel) and not RE_SIGNATURE.search(text):
            hits["E3"].append(rel)
        if RE_CORS_STAR.search(text) and RE_CREDENTIALS.search(text):
            hits["E4"].append(f"{rel}:{first_line(text, RE_CORS_STAR)}")
        if RE_COOKIE_SET.search(text) and not RE_COOKIE_FLAGS.search(text):
            hits["F2"].append(f"{rel}:{first_line(text, RE_COOKIE_SET)}")
        if (RE_AUTH_ROUTE.search(rel) or RE_LOGIN_ROUTE.search(text)) and not RE_RATE_LIMIT.search(text):
            hits["G1"].append(rel)
        if RE_CLIENT_IP_HEADER.search(text) or RE_FWD_CLEAR.search(text):
            hits["G8"].append(f"{rel}:{first_line(text, RE_CLIENT_IP_HEADER) or first_line(text, RE_FWD_CLEAR)}")
        if RE_HASH_CALL.search(text) and not RE_CONCURRENCY_CAP.search(text):
            hits["G4"].append(f"{rel}:{first_line(text, RE_HASH_CALL)}")
        if RE_RAW_SQL.search(text):
            hits["H3"].append(f"{rel}:{first_line(text, RE_RAW_SQL)}")
        if RE_JWT_DECODE.search(text) and not RE_JWT_VERIFY.search(text):
            hits["J1"].append(f"{rel}:{first_line(text, RE_JWT_DECODE)}")
        if RE_SECRET_LOG.search(text):
            hits["J6"].append(f"{rel}:{first_line(text, RE_SECRET_LOG)}")
        if RE_STACK_TO_CLIENT.search(text):
            hits["M1"].append(f"{rel}:{first_line(text, RE_STACK_TO_CLIENT)}")
        if RE_SSRF.search(text):
            hits["I1"].append(f"{rel}:{first_line(text, RE_SSRF)}")
        if RE_LOCAL_REDIRECT.search(text):
            hits["H4"].append(f"{rel}:{first_line(text, RE_LOCAL_REDIRECT)}")

    spec = {
        "A1": ("No service keys in public variables", "CRITICAL"),
        "B1": ("Service-role key outside server code", "CRITICAL"),
        "D2": ("(not scanned)", "-"),
        "E1": ("Debug, test or admin route in the source tree", "HIGH"),
        "E3": ("Webhook handler with no signature check nearby", "HIGH"),
        "E4": ("Wildcard CORS together with credentials", "HIGH"),
        "F2": ("Cookie set with no HttpOnly flag nearby", "HIGH"),
        "G1": ("Auth route with no rate limiting nearby", "MEDIUM"),
        "H2": ("Unsanitized HTML output", "HIGH"),
        "H3": ("SQL built by string concatenation", "CRITICAL"),
        "H4": ("Redirect target parameter (verify it is local-only)", "MEDIUM"),
        "I1": ("Outbound request built from request input (SSRF)", "HIGH"),
        "J1": ("Token decoded without verification", "CRITICAL"),
        "J6": ("Secret-like value passed to a log call", "HIGH"),
        "M1": ("Stack trace in a response body", "MEDIUM"),
        "G8": ("Client IP taken from a header without a trusted-proxy check (review: the header can be forged)", "HIGH"),
        "G4": ("Password hashing call with no concurrency cap in the file (review: N parallel logins multiply memory)", "HIGH"),
    }
    for check_id, found in hits.items():
        if check_id == "D2":
            continue
        name, severity = spec[check_id]
        if found:
            rows.append((check_id, name, "FAIL", severity, "; ".join(found[:5]) + (" ..." if len(found) > 5 else "")))
        else:
            rows.append((check_id, name, "PASS", "-", "no pattern hit"))
    return rows


def render(rows) -> str:
    out = ["| ID | Check | Status | Severity | Evidence |", "|---|---|---|---|---|"]
    out += [f"| {i} | {c} | {s} | {v} | {e} |" for i, c, s, v, e in rows]
    out += ["", "Mechanical pass only. Items marked NOT VERIFIED or FAIL need a reading of the code."]
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".")
    args = ap.parse_args(argv)
    rows = scan(Path(args.root).resolve())
    if rows is None:
        print("NOT VERIFIED: no source files found", file=sys.stderr)
        return 2
    print(render(rows))
    return 1 if any(r[2] == "FAIL" for r in rows) else 0


if __name__ == "__main__":
    sys.exit(main())
