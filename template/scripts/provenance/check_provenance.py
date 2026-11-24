#!/usr/bin/env python3
"""Check PROVENANCE.md files: required fields, and (optionally) whether the source moved.

Each skill or extra folder with an outside origin has a PROVENANCE.md with "- key: value" lines.
Offline (default): checks the fields. With --online: asks the source repository for its HEAD
with `git ls-remote` and reports "REVIEW" when the recorded commit differs. The HEAD comparison
is a signal that the source moved, not proof that the copied file changed.

Usage:
  python3 scripts/provenance/check_provenance.py [--root .] [--online]

Exit: 0 all recorded, 1 field missing or upstream moved (REVIEW), 2 online check could not run.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REQUIRED = ("type", "source", "license", "commit", "last_checked")
FIELD = re.compile(r"^- ([a-z_]+):\s*(.+)$")
NOT_RECORDED = "NOT VERIFIED"
SCAN = ("template/.agents/skills", "extras")


def parse(text: str) -> dict[str, str]:
    return {m.group(1): m.group(2).strip() for m in (FIELD.match(line) for line in text.splitlines()) if m}


def upstream_head(source: str) -> str | None:
    """Return the HEAD commit of a git source, or None when it cannot be read."""
    try:
        out = subprocess.run(["git", "ls-remote", source, "HEAD"], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if out.returncode != 0 or not out.stdout.strip():
        return None
    return out.stdout.split()[0]


def check(path: Path, online: bool, head_of=upstream_head) -> list[tuple[str, str]]:
    """Return (status, message) rows for one PROVENANCE.md."""
    fields = parse(path.read_text(encoding="utf-8"))
    rows = []
    missing = [k for k in REQUIRED if k not in fields]
    if missing:
        rows.append(("REVIEW", f"missing fields: {', '.join(missing)}"))
    commit = fields.get("commit", NOT_RECORDED)
    if commit.startswith(NOT_RECORDED):
        rows.append(("NOT VERIFIED", "no commit recorded; upstream cannot be compared"))
    elif online and fields.get("source", "").startswith(("http", "git@")):
        head = head_of(fields["source"])
        if head is None:
            rows.append(("NOT VERIFIED", "source could not be reached"))
        elif not head.startswith(commit):
            rows.append(("REVIEW", f"source HEAD {head[:7]} differs from recorded {commit[:7]}"))
    if not rows:
        rows.append(("OK", "fields recorded"))
    return rows


def find(root: Path):
    for rel in SCAN:
        for p in sorted((root / rel).rglob("PROVENANCE.md")):
            yield p


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".")
    ap.add_argument("--online", action="store_true", help="ask each git source for its HEAD")
    args = ap.parse_args(argv)
    root = Path(args.root).resolve()
    worst = 0
    for path in find(root):
        for status, message in check(path, args.online):
            print(f"{status:<13} {path.parent.relative_to(root).as_posix()}: {message}")
            if status == "REVIEW":
                worst = max(worst, 1)
            if status == "NOT VERIFIED" and worst == 0:
                worst = 2
    return worst


if __name__ == "__main__":
    sys.exit(main())
