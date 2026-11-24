#!/usr/bin/env python3
"""Triage the backlog: one TSV row per item, with only facts read from the file.

It never edits an item and never classifies by model. Each flag is a
text match you can check by opening the file:

  done-with-open-items   status is done but the body still has `- [ ]`
  state-in-title         the title carries the state (`[x]`, `~~`, "DONE")
  empty-body             nothing after the metadata line

Usage:
  python3 scripts/backlog/triage_backlog.py [--root .] [--tsv out/triage.tsv]
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

from backlog_lib import load_items

RE_STATE_IN_TITLE = re.compile(r"\[x\]|~~|\bDONE\b|\bdone\b", re.I)
COLUMNS = ["id", "epic", "status", "title", "open_boxes", "done_boxes", "flags"]


def flags_for(item) -> list[str]:
    flags = []
    if item.is_done and item.open_boxes:
        flags.append("done-with-open-items")
    if RE_STATE_IN_TITLE.search(item.title):
        flags.append("state-in-title")
    if not item.body.strip():
        flags.append("empty-body")
    return flags


def rows(root: Path):
    items, _broken = load_items(root)
    for item in sorted(items, key=lambda i: (i.epic, i.item_id)):
        done = len(re.findall(r"^\s*- \[x\]", item.body, re.I | re.M))
        yield [
            item.item_id,
            item.epic,
            item.status,
            item.title.replace("\t", " "),
            str(item.open_boxes),
            str(done),
            ";".join(flags_for(item)),
        ]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".")
    ap.add_argument("--tsv", type=Path, help="write the table here (parent folders are created)")
    args = ap.parse_args(argv)
    data = list(rows(Path(args.root).resolve()))

    flag_counts = Counter(f for r in data for f in r[-1].split(";") if f)
    print(f"{len(data)} item(s)")
    for flag, n in sorted(flag_counts.items()):
        print(f"  {flag}: {n}")

    if args.tsv:
        args.tsv.parent.mkdir(parents=True, exist_ok=True)
        lines = ["\t".join(COLUMNS)] + ["\t".join(r) for r in data]
        args.tsv.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"wrote {args.tsv}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
