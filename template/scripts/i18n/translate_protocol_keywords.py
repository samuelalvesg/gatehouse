#!/usr/bin/env python3
"""Replace protocol keywords (uppercase tokens that agents parse) with their English forms.

Only whole uppercase tokens are replaced, so ordinary prose (lowercase words, sentences) is
never touched. The mapping lives in protocol_keywords.json next to this script.

Usage:
  python3 scripts/i18n/translate_protocol_keywords.py --root . [--apply] [--verify]

Default is a dry run: it counts the replacements per file and writes nothing.
--verify exits 1 when any old keyword is still present in the target files.
Exit: 0 ok, 1 old keyword still present (with --verify), 2 mapping or root not found.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGETS = ("AGENTS.md", "CLAUDE.md", ".agents/**/*.md", ".claude/**/*.md", "template/**/*.md", "profiles/**/*.md")


def load_mapping(path: Path) -> dict[str, str]:
    return json.loads(path.read_text(encoding="utf-8"))


def pattern_for(keyword: str) -> re.Pattern:
    # A keyword is a whole token: not preceded or followed by a letter, digit or underscore.
    return re.compile(r"(?<![0-9A-Za-zÀ-ÿ_])" + re.escape(keyword) + r"(?![0-9A-Za-zÀ-ÿ_])")


def translate(text: str, mapping: dict[str, str]) -> tuple[str, int]:
    count = 0
    for old in sorted(mapping, key=len, reverse=True):
        text, n = pattern_for(old).subn(mapping[old], text)
        count += n
    return text, count


def leftovers(text: str, mapping: dict[str, str]) -> list[str]:
    return [old for old in mapping if pattern_for(old).search(text)]


def files(root: Path):
    seen = set()
    for glob in TARGETS:
        for p in sorted(root.glob(glob)):
            if p.is_file() and p not in seen:
                seen.add(p)
                yield p


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".")
    ap.add_argument("--mapping", type=Path, default=HERE / "protocol_keywords.json")
    ap.add_argument("--apply", action="store_true", help="write the changes (default: dry run)")
    ap.add_argument("--verify", action="store_true", help="fail if an old keyword is still present")
    args = ap.parse_args(argv)
    root = Path(args.root).resolve()
    if not root.is_dir() or not args.mapping.is_file():
        print("root or mapping not found", file=sys.stderr)
        return 2
    mapping = load_mapping(args.mapping)
    total, remaining = 0, []
    for path in files(root):
        text = path.read_text(encoding="utf-8")
        new, n = translate(text, mapping)
        if n:
            total += n
            print(f"{n:4d}  {path.relative_to(root).as_posix()}")
            if args.apply:
                path.write_text(new, encoding="utf-8")
        left = leftovers(new if args.apply else text, mapping) if (args.verify or args.apply) else []
        if left:
            remaining.append((path.relative_to(root).as_posix(), left))
    print(f"{total} replacement(s) {'written' if args.apply else 'pending (dry run)'}")
    if args.verify or args.apply:
        for name, left in remaining:
            print(f"still present in {name}: {', '.join(left)}")
        if remaining:
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
