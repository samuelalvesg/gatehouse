#!/usr/bin/env python3
"""One-time migration: split a single-file backlog into one file per item.

Each `## ` heading starts an item. Text before the first heading becomes the
preamble of the new index. Dry run by default; --write applies it.

Safety: before writing, every non-empty source line must reappear in the
output (the generated metadata, title and index rows are the only additions).
If any line would be lost, nothing is written.

Usage:
  python3 scripts/backlog/split_backlog.py --source old-backlog.md --epic misc
  python3 scripts/backlog/split_backlog.py --source old-backlog.md --epic misc --write
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from collections import Counter
from datetime import date
from pathlib import Path

from backlog_lib import ALLOWED_STATUSES, INDEX_PATH, ITEMS_DIR


def slugify(text: str) -> str:
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-")[:80] or "item"


def split(text: str):
    """Return (preamble, [(title, body_lines)])."""
    preamble, sections, current = [], [], None
    for line in text.splitlines():
        if line.startswith("## "):
            current = (line[3:].strip(), [])
            sections.append(current)
        elif current is None:
            preamble.append(line)
        else:
            current[1].append(line)
    return preamble, sections


def plan(root: Path, source: Path, epic: str, status: str):
    preamble, sections = split(source.read_text(encoding="utf-8"))
    today = date.today().isoformat()
    files, rows, generated = {}, [], Counter()
    for n, (title, body) in enumerate(sections, start=1):
        item_id = str(n)
        slug = slugify(title) or f"item-{n}"
        rel = f"{epic}/{slug}.md"
        meta = f"> **Epic:** `{epic}` · **ID:** `{item_id}` · **Status:** {status} · **Registered:** {today}"
        head = [f"# {title}", "", meta, ""]
        files[root / ITEMS_DIR / rel] = head + body
        generated.update([f"# {title}", meta])
        rows.append(f"| `{item_id}` | {epic} | {title} | {status} | [open](backlog/{rel}) |")
    index_lines = preamble + ["", "| ID | Epic | Title | Status | Link |", "|---|---|---|---|---|"] + rows
    return files, index_lines, generated, sections


def lost_lines(source_text: str, files: dict, index_lines: list[str], generated: Counter) -> Counter:
    expected = Counter(l for l in source_text.splitlines() if l.strip() and not l.startswith("## "))
    actual = Counter()
    for lines in list(files.values()) + [index_lines]:
        actual.update(l for l in lines if l.strip())
    actual.subtract(generated)
    actual.subtract(Counter(l for l in index_lines if l.startswith("| `") or l.startswith("| ID |") or l == "|---|---|---|---|---|"))
    return expected - actual


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".")
    ap.add_argument("--source", type=Path, required=True)
    ap.add_argument("--epic", required=True)
    ap.add_argument("--status", default=ALLOWED_STATUSES[0])
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args(argv)
    root = Path(args.root).resolve()
    source = args.source.resolve()
    if source == (root / INDEX_PATH).resolve():
        print("source is the index itself; move the old file aside first", file=sys.stderr)
        return 2

    files, index_lines, generated, sections = plan(root, source, args.epic, args.status)
    lost = lost_lines(source.read_text(encoding="utf-8"), files, index_lines, generated)
    print(f"{len(sections)} item(s) found; {sum(lost.values())} source line(s) would be lost")
    if lost:
        for line, n in list(lost.items())[:10]:
            print(f"  lost x{n}: {line[:100]}")
        return 1
    if not args.write:
        print("dry run: nothing written (use --write)")
        return 0
    if (root / INDEX_PATH).exists():
        print(f"index exists: {INDEX_PATH}; remove or move it first", file=sys.stderr)
        return 2
    for path, lines in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    (root / INDEX_PATH).write_text("\n".join(index_lines).rstrip() + "\n", encoding="utf-8")
    print(f"wrote {len(files)} item file(s) and {INDEX_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
