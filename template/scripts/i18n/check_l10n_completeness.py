#!/usr/bin/env python3
"""Check that every translation file has the same keys as the reference file. Standard library only.

The reference file (for example app_en.arb) is the source of truth: a new string is added there
first. Keys that start with "@" are metadata and are ignored. A missing key is a violation; an
extra key (a key the reference does not have) is reported as well.

Usage:
  python3 scripts/i18n/check_l10n_completeness.py --dir lib/l10n --reference app_en.arb --pattern "app_*.arb"

Exit: 0 all translations complete, 1 missing or extra keys, 2 reference not found.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def keys(path: Path) -> set[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return {k for k in data if not k.startswith("@")}


def check(folder: Path, reference: str, pattern: str):
    ref = folder / reference
    if not ref.is_file():
        return None
    base = keys(ref)
    report = []
    for path in sorted(folder.glob(pattern)):
        if path.name == reference:
            continue
        have = keys(path)
        missing, extra = sorted(base - have), sorted(have - base)
        if missing or extra:
            report.append((path.name, missing, extra))
    return report


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", type=Path, required=True)
    ap.add_argument("--reference", default="app_en.arb")
    ap.add_argument("--pattern", default="app_*.arb")
    args = ap.parse_args(argv)
    report = check(args.dir, args.reference, args.pattern)
    if report is None:
        print(f"NOT VERIFIED: reference {args.reference} not found in {args.dir}")
        return 2
    for name, missing, extra in report:
        if missing:
            print(f"{name}: missing {len(missing)} key(s): {', '.join(missing[:10])}")
        if extra:
            print(f"{name}: extra {len(extra)} key(s): {', '.join(extra[:10])}")
    if report:
        print(f"{len(report)} translation file(s) out of sync with {args.reference}")
        return 1 if any(m for _, m, _ in report) or any(e for _, _, e in report) else 0
    print("all translations have the reference keys")
    return 0


if __name__ == "__main__":
    sys.exit(main())
