#!/usr/bin/env python3
"""Change an item's status in its file and in its index row, together.

Refuses to mark an item done while it still has open checkboxes: done means
every subitem is done (see the backlog-items skill).

Usage:
  python3 scripts/backlog/set_status.py <slug-or-path> --status "✅ Done" [--root .]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from backlog_lib import (
    ALLOWED_STATUSES,
    DONE_PREFIX,
    INDEX_PATH,
    ITEMS_DIR,
    RE_META,
    load_items,
    status_is_allowed,
)


def find_item(root: Path, ref: str) -> Path | None:
    direct = Path(ref) if Path(ref).is_absolute() else root / ref
    if direct.is_file():
        return direct
    matches = [p for p in (root / ITEMS_DIR).rglob("*.md") if p.stem == Path(ref).stem]
    return matches[0] if len(matches) == 1 else None


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ref", help="file path, or the file name without .md")
    ap.add_argument("--status", required=True, help=f"one of: {', '.join(ALLOWED_STATUSES)}")
    ap.add_argument("--root", default=".")
    args = ap.parse_args(argv)
    root = Path(args.root).resolve()

    if not status_is_allowed(args.status):
        print(f"status not allowed: {args.status}", file=sys.stderr)
        return 2
    path = find_item(root, args.ref)
    if path is None:
        print(f"item not found or ambiguous: {args.ref}", file=sys.stderr)
        return 2

    item = next((i for i in load_items(root)[0] if i.path.resolve() == path.resolve()), None)
    if item is None:
        print(f"no metadata line in {path.relative_to(root)}", file=sys.stderr)
        return 2
    if args.status.startswith(DONE_PREFIX) and item.open_boxes:
        print(f"refused: {item.open_boxes} open checkbox(es); finish them or keep the status partial", file=sys.stderr)
        return 1

    text = path.read_text(encoding="utf-8")
    m = RE_META.search(text)
    new_meta = m.group(0).replace(f"**Status:** {item.status}", f"**Status:** {args.status}", 1)
    path.write_text(text[: m.start()] + new_meta + text[m.end():], encoding="utf-8")

    index = root / INDEX_PATH
    rel_link = path.relative_to(root / INDEX_PATH.parent).as_posix()
    lines = index.read_text(encoding="utf-8").splitlines(keepends=True)
    changed = 0
    for i, line in enumerate(lines):
        if f"]({rel_link})" in line and f"| {item.status} |" in line:
            lines[i] = line.replace(f"| {item.status} |", f"| {args.status} |", 1)
            changed += 1
    if changed != 1:
        print(f"warning: {changed} index row(s) updated for {rel_link}; check the index", file=sys.stderr)
    index.write_text("".join(lines), encoding="utf-8")
    print(f"{path.relative_to(root)}: {item.status} -> {args.status}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
