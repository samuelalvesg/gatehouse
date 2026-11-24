#!/usr/bin/env python3
"""Report links and repository paths in Markdown files that point to nothing.

Checks two forms:
  [text](relative/path.md)        resolved from the file's own folder
  `docs/some/path.md`             backticked paths, resolved from the repo root

External URLs and in-page anchors are ignored.

Usage:
  python3 scripts/backlog/check_doc_paths.py [--root .]

Exit codes: 0 clean, 1 broken paths found.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

RE_LINK = re.compile(r"\]\(([^)\s]+)\)")
RE_TICK = re.compile(r"`((?:docs|scripts|src|lib|test)/[\w./-]+)`")
SKIP_DIRS = {".git", "node_modules", "build", ".dart_tool"}


def markdown_files(root: Path):
    for p in root.rglob("*.md"):
        if not SKIP_DIRS.intersection(p.parts):
            yield p


def broken_in(root: Path, md: Path) -> list[str]:
    text = md.read_text(encoding="utf-8", errors="replace")
    out = []
    for target in RE_LINK.findall(text):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        clean = target.split("#", 1)[0]
        if clean and not (md.parent / clean).exists():
            out.append(f"link -> {target}")
    for path in RE_TICK.findall(text):
        if not (root / path).exists():
            out.append(f"path `{path}`")
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".")
    args = ap.parse_args(argv)
    root = Path(args.root).resolve()
    total = 0
    for md in sorted(markdown_files(root)):
        for problem in broken_in(root, md):
            total += 1
            print(f"{md.relative_to(root)}: {problem}")
    print(f"{total} broken path(s)")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
