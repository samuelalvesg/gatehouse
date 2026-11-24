#!/usr/bin/env python3
"""Documentation freshness gate. Standard library only.

Checks:
  G1  each generated file equals a fresh run of its generator
  G2  canonical docs contain no statement matched by a rule in docs/freshness.json
  G3  each generated file starts with a GENERATED marker

Exit: 0 clean, 1 violations, 2 inputs missing (not verified; never green).
Escape hatch: a line containing "docs-fresh: ignore" is skipped by G2.

Generators live in scripts/docs/generators/*.py. Each one defines OUTPUT
(path relative to the repository root) and generate(root) -> str, and raises
FileNotFoundError when its inputs are missing.

docs/freshness.json:
  {"canonical": ["README.md", "docs/API.md"],
   "rules": [{"id": "R1", "pattern": "\\\\b\\\\d+ tests\\\\b", "message": "typed test count"}]}
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

IGNORE = "docs-fresh: ignore"
MARKER = "GENERATED"
HERE = Path(__file__).resolve().parent


def load_generators(folder: Path) -> dict:
    gens = {}
    for path in sorted(folder.glob("*.py")):
        if path.name.startswith("_"):
            continue
        spec = importlib.util.spec_from_file_location(path.stem, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        gens[module.OUTPUT] = module.generate
    return gens


def load_config(root: Path) -> dict:
    path = root / "docs" / "freshness.json"
    if not path.is_file():
        return {"canonical": [], "rules": []}
    return json.loads(path.read_text(encoding="utf-8"))


def check(root: Path, generators_dir: Path = HERE / "generators"):
    """Return (violations, missing_inputs)."""
    bad, missing = [], []
    for rel, generate in load_generators(generators_dir).items():
        path = root / rel
        try:
            fresh = generate(root)
        except FileNotFoundError as err:
            missing.append(f"{rel}: {err}")
            continue
        if not path.is_file():
            bad.append(f"G1 {rel}: missing (run the generator with --write)")
            continue
        text = path.read_text(encoding="utf-8")
        if text != fresh:
            bad.append(f"G1 {rel}: out of date (run the generator with --write)")
        first = text.splitlines()[0] if text else ""
        if MARKER not in first:
            bad.append(f"G3 {rel}: no {MARKER} marker on the first line")

    config = load_config(root)
    rules = [(r["id"], re.compile(r["pattern"]), r["message"]) for r in config["rules"]]
    for rel in config["canonical"]:
        path = root / rel
        if not path.is_file():
            continue
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if IGNORE in line:
                continue
            for rid, rx, message in rules:
                if rx.search(line):
                    bad.append(f"G2/{rid} {rel}:{n}: {message}")
    return bad, missing


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=str(HERE.parents[1]))
    args = ap.parse_args(argv)
    bad, missing = check(Path(args.root).resolve())
    for m in missing:
        print(f"NOT VERIFIED: {m}", file=sys.stderr)
    for b in bad:
        print(f"✗ {b}")
    if bad:
        print(f"❌ {len(bad)} violation(s)")
        return 1
    if missing:
        return 2
    print("✅ docs up to date (generators and freshness rules)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
