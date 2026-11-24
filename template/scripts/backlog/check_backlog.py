#!/usr/bin/env python3
"""Check a file-per-item backlog and its index.

Checks:
  C1  every item file has a metadata line (epic, id, status)
  C2  the epic in the metadata matches the folder the file lives in
  C3  the status is one of ALLOWED_STATUSES
  C4  every index row points to an existing item file
  C5  every item file is listed in the index (no orphans)
  C6  the status in an index row equals the status in the item file
  C7  no done item is listed in the index (the index is the open queue)
  C8  no done item has an open checkbox (done means 100% of the subitems)

Usage:
  python3 scripts/backlog/check_backlog.py [--root .] [--verbose]

Exit codes: 0 clean, 1 violations found, 2 usage error.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from backlog_lib import (
    INDEX_PATH,
    ITEMS_DIR,
    index_rows,
    load_items,
    status_is_allowed,
)


def run(root: Path) -> list[str]:
    problems: list[str] = []
    if not (root / INDEX_PATH).is_file():
        return [f"index not found: {INDEX_PATH}"]
    if not (root / ITEMS_DIR).is_dir():
        return [f"items folder not found: {ITEMS_DIR}"]

    items, broken = load_items(root)
    for path in broken:
        problems.append(f"C1 no metadata line: {path.relative_to(root)}")

    by_path = {}
    for item in items:
        rel = item.path.relative_to(root / ITEMS_DIR)
        folder = rel.parts[0] if len(rel.parts) > 1 else ""
        by_path[item.path.resolve()] = item
        if folder != item.epic:
            problems.append(f"C2 epic `{item.epic}` in a folder `{folder}`: {rel}")
        if not status_is_allowed(item.status):
            problems.append(f"C3 unknown status `{item.status}`: {rel}")
        if item.is_done and item.open_boxes:
            problems.append(f"C8 done with {item.open_boxes} open checkbox(es): {rel}")

    listed = set()
    for item_id, _epic, _title, status, link in index_rows(root):
        target = (root / INDEX_PATH.parent / link).resolve()
        listed.add(target)
        item = by_path.get(target)
        if item is None:
            problems.append(f"C4 index row `{item_id}` points to no item: {link}")
            continue
        if status != item.status:
            problems.append(
                f"C6 index `{status}` != item `{item.status}`: {item.path.relative_to(root)}"
            )
        if item.is_done:
            problems.append(f"C7 done item in the index: {item.path.relative_to(root)}")

    for target, item in by_path.items():
        if target not in listed:
            problems.append(f"C5 not in the index: {item.path.relative_to(root)}")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".", help="repository root (default: current directory)")
    ap.add_argument("--verbose", action="store_true", help="also list the checks that ran")
    args = ap.parse_args(argv)
    root = Path(args.root).resolve()
    problems = run(root)
    for p in problems:
        print(p)
    if args.verbose or not problems:
        print(f"{len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
