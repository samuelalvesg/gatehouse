#!/usr/bin/env python3
"""Fail when a test run skipped more tests than allowed. Standard library only.

Reads the summary line of a test runner (dotnet/vstest, pytest, jest, and their Portuguese
dotnet output) from a file or stdin. A skipped test is a test that did not run, so a green
summary with skips is not a full pass.

Usage:
  dotnet test ... > run.log; python3 scripts/tests/check_skipped.py --file run.log --allow 0

Exit: 0 skipped <= allowed, 1 too many skipped, 2 no summary found (not verified).
"""

from __future__ import annotations

import argparse
import re
import sys

PATTERNS = [
    re.compile(r"(?i)skipped\s*[:=]\s*(\d+)"),
    re.compile(r"(?i)ignorado[s]?\s*[:=]\s*(\d+)"),
    re.compile(r"(\d+)\s+skipped"),
    re.compile(r"(\d+)\s+ignorado[s]?"),
]


def skipped_count(text: str) -> int | None:
    found = [int(m.group(1)) for rx in PATTERNS for m in rx.finditer(text)]
    return max(found) if found else None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", help="test output file (default: stdin)")
    ap.add_argument("--allow", type=int, default=0, help="how many skipped tests are accepted")
    args = ap.parse_args(argv)
    text = open(args.file, encoding="utf-8", errors="replace").read() if args.file else sys.stdin.read()
    count = skipped_count(text)
    if count is None:
        print("NOT VERIFIED: no test summary with a skipped count was found")
        return 2
    if count > args.allow:
        print(f"FAIL: {count} skipped test(s), {args.allow} allowed")
        return 1
    print(f"OK: {count} skipped, {args.allow} allowed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
