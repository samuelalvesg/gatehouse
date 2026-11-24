#!/usr/bin/env python3
"""Keep check IDs stable while skills are edited. Standard library only.

Two jobs:
  integrity (default): every ID the scanners and the index cite must exist in the skill that owns it.
  snapshot:            record every check ID and a hash of its text, so a later edit shows what was
                       removed or reworded. Run once before an edit, then compare after.

Checks are bold list items in a skill: "- **G4** Password hashing ...".

Usage:
  python3 scripts/skills/check_skill_ids.py [--root .]                  integrity (exit 1 on a broken citation)
  python3 scripts/skills/check_skill_ids.py --snapshot out.json        write the current IDs and text hashes
  python3 scripts/skills/check_skill_ids.py --compare before.json      list removed and reworded IDs
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ITEM = re.compile(r"^- \*\*([A-Z]{1,2}\d{1,2})\*\*\s*(.*)$", re.M)
CITED_IN_CODE = re.compile(r'"([A-Z]{1,2}\d{1,2})"')
OWNER = "web-app-security-audit"  # the scanner's IDs belong to this skill


def items(skills_dir: Path) -> dict[str, dict[str, str]]:
    """skill name -> {id: text of the item}."""
    out = {}
    for path in sorted(skills_dir.glob("*/SKILL.md")):
        text = path.read_text(encoding="utf-8")
        out[path.parent.name] = {m.group(1): m.group(2).strip() for m in ITEM.finditer(text)}
    return out


def cited_by_scanner(root: Path) -> set[str]:
    path = root / "scripts" / "security" / "scan_web_patterns.py"
    if not path.is_file():
        path = root / "template" / "scripts" / "security" / "scan_web_patterns.py"
    if not path.is_file():
        return set()
    return set(CITED_IN_CODE.findall(path.read_text(encoding="utf-8")))


def integrity(root: Path, skills_dir: Path) -> list[str]:
    known = items(skills_dir)
    if OWNER not in known:
        return [f"owner skill {OWNER} not found"]
    problems = []
    for cid in sorted(cited_by_scanner(root) - set(known[OWNER])):
        problems.append(f"scanner cites {cid}, which {OWNER} does not define")
    return problems


def snapshot(skills_dir: Path) -> dict:
    return {
        skill: {cid: hashlib.sha256(text.encode("utf-8")).hexdigest()[:12] for cid, text in ids.items()}
        for skill, ids in items(skills_dir).items()
    }


def compare(before: dict, after: dict) -> list[str]:
    out = []
    for skill in sorted(set(before) | set(after)):
        b, a = before.get(skill, {}), after.get(skill, {})
        for cid in sorted(set(b) - set(a)):
            out.append(f"REMOVED  {skill} {cid}")
        for cid in sorted(set(a) - set(b)):
            out.append(f"ADDED    {skill} {cid}")
        for cid in sorted(set(a) & set(b)):
            if a[cid] != b[cid]:
                out.append(f"REWORDED {skill} {cid}")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".")
    ap.add_argument("--skills", default=None, help="skills folder (default: <root>/.agents/skills or template/.agents/skills)")
    ap.add_argument("--snapshot", type=Path, help="write the snapshot JSON here")
    ap.add_argument("--compare", type=Path, help="compare the current skills with a snapshot file")
    args = ap.parse_args(argv)
    root = Path(args.root).resolve()
    skills_dir = Path(args.skills) if args.skills else next(
        (p for p in (root / ".agents" / "skills", root / "template" / ".agents" / "skills") if p.is_dir()), None
    )
    if skills_dir is None:
        print("no skills folder found", file=sys.stderr)
        return 2
    if args.snapshot:
        args.snapshot.write_text(json.dumps(snapshot(skills_dir), indent=2, sort_keys=True), encoding="utf-8")
        print(f"snapshot written: {args.snapshot}")
        return 0
    if args.compare:
        changes = compare(json.loads(args.compare.read_text(encoding="utf-8")), snapshot(skills_dir))
        print("\n".join(changes) if changes else "no change in IDs or text")
        return 1 if any(c.startswith("REMOVED") for c in changes) else 0
    problems = integrity(root, skills_dir)
    print("\n".join(problems) if problems else "all cited IDs exist")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
