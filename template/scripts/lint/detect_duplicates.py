#!/usr/bin/env python3
"""Find blocks of code repeated across files. Language-agnostic, standard library only.

Each file is reduced to its non-blank, non-comment lines (whitespace collapsed). Any run of
`--window` consecutive lines that appears in two or more different files is reported with
its locations. Use it before writing a helper: if the block already exists, reuse it.

Usage:
  python3 scripts/lint/detect_duplicates.py --root src --window 8 --ext .py .dart .cs .ts

Exit: 0 no duplicate block, 1 duplicates found.
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

COMMENT_PREFIXES = ("//", "#", "--", "/*", "*", "<!--")
SKIP = {".git", "node_modules", "build", "bin", "obj", ".dart_tool", "__pycache__", "worktrees"}


def normalized(path: Path) -> list[tuple[int, str]]:
    out = []
    for n, raw in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        line = " ".join(raw.split())
        if line and not line.startswith(COMMENT_PREFIXES):
            out.append((n, line))
    return out


def duplicates(root: Path, window: int, exts: set[str]):
    index: dict[tuple[str, ...], list[tuple[str, int]]] = defaultdict(list)
    for p in sorted(root.rglob("*")):
        if not p.is_file() or p.suffix not in exts or set(p.relative_to(root).parts) & SKIP:
            continue
        lines = normalized(p)
        for i in range(len(lines) - window + 1):
            block = tuple(text for _, text in lines[i:i + window])
            index[block].append((p.relative_to(root).as_posix(), lines[i][0]))
    result = []
    for block, where in index.items():
        files = {f for f, _ in where}
        if len(files) >= 2:
            result.append((block, sorted(set(where))))
    return result


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".")
    ap.add_argument("--window", type=int, default=8)
    ap.add_argument("--ext", nargs="+", default=[".py", ".dart", ".cs", ".ts", ".js", ".rs", ".java", ".kt"])
    args = ap.parse_args(argv)
    found = duplicates(Path(args.root).resolve(), args.window, set(args.ext))
    for block, where in found[:50]:
        print(f"{len(where)} places: " + ", ".join(f"{f}:{n}" for f, n in where[:4]))
        print(f"    {block[0][:100]}")
    print(f"{len(found)} repeated block(s) of {args.window} lines")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
