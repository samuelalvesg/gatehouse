#!/usr/bin/env python3
"""Create an item file and its index row. Never edits an existing item.

Usage:
  python3 scripts/backlog/new_item.py --epic core --title "Add export to CSV" \
      --status "📝 Registered" [--id 42] [--root .]

Refuses to run when the status is not in ALLOWED_STATUSES, when the file
already exists, or when the index has no table to append to.
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

from backlog_lib import ALLOWED_STATUSES, INDEX_PATH, ITEMS_DIR, status_is_allowed


def slugify(text: str) -> str:
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-")
    return slug[:80].rstrip("-") or "item"


def item_text(epic: str, item_id: str, title: str, status: str, today: str) -> str:
    return (
        f"# {title}\n\n"
        f"> **Epic:** `{epic}` · **ID:** `{item_id}` · **Status:** {status} · **Registered:** {today}\n\n"
        "---\n\n"
        "## Context\n\n"
        "What the item is and why it matters. Facts only; mark what was not checked.\n\n"
        "## Subitems\n\n"
        "- [ ] First concrete step\n"
    )


def index_line(item_id: str, epic: str, title: str, status: str, link: str) -> str:
    return f"| `{item_id}` | {epic} | {title} | {status} | [open]({link}) |"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".")
    ap.add_argument("--epic", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--status", default=ALLOWED_STATUSES[0], help=f"one of: {', '.join(ALLOWED_STATUSES)}")
    ap.add_argument("--id", default="—", dest="item_id")
    args = ap.parse_args(argv)

    root = Path(args.root).resolve()
    if not status_is_allowed(args.status):
        print(f"status not allowed: {args.status}", file=sys.stderr)
        return 2
    index = root / INDEX_PATH
    if not index.is_file() or "| `" not in index.read_text(encoding="utf-8"):
        print(f"index has no table: {INDEX_PATH}", file=sys.stderr)
        return 2

    folder = root / ITEMS_DIR / args.epic
    path = folder / f"{slugify(args.title)}.md"
    if path.exists():
        print(f"already exists: {path.relative_to(root)}", file=sys.stderr)
        return 2

    folder.mkdir(parents=True, exist_ok=True)
    path.write_text(item_text(args.epic, args.item_id, args.title, args.status, date.today().isoformat()), encoding="utf-8")

    link = path.relative_to(root / INDEX_PATH.parent).as_posix()
    lines = index.read_text(encoding="utf-8").splitlines(keepends=True)
    last_row = max(i for i, l in enumerate(lines) if l.startswith("| `"))
    lines.insert(last_row + 1, index_line(args.item_id, args.epic, args.title, args.status, link) + "\n")
    index.write_text("".join(lines), encoding="utf-8")

    print(f"created {path.relative_to(root)} and its index row")
    return 0


if __name__ == "__main__":
    sys.exit(main())
