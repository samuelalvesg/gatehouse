#!/usr/bin/env python3
"""Look for prompt-injection and exfiltration patterns in agent instruction files.

Agent skills and agent definitions are instructions that an agent executes.
This scanner flags lines that try to give the agent a new authority, send data
out, read credentials, change the agent's own configuration, or chain shell
commands in a risky way. It is a lead generator: every hit is reviewed by a
person, and a defensive line that describes an attack is excluded by the
markers below.

Pattern groups follow published lists of agent-skill attack classes
(authority override, credential harvesting, system manipulation, tool-chain abuse).

Usage:
  python3 scripts/security/scan_skill_injection.py [--root .]

Exit: 0 no unexcluded hit, 1 hits to review.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SCAN_DIRS = (".agents", ".claude")
SCAN_NAMES = ("SKILL.md", "AGENTS.md", "CLAUDE.md")

PATTERNS = [
    ("authority", "override", re.compile(r"ignore (all )?(the )?previous instructions|disregard (your|all previous)|forget your instructions|system override|new directive|you are now (a|in)\b", re.I)),
    ("exfiltration", "send data out", re.compile(r"send (it |this |the \w+ )?to https?://|curl\s+-X\s+POST|wget\s+--post", re.I)),
    ("exfiltration", "webhook", re.compile(r"discord\.com/api/webhooks|hooks\.slack\.com/services|api\.telegram\.org", re.I)),
    ("credentials", "read secrets", re.compile(r"(cat|read|print|upload|send)\b.{0,40}(~/\.ssh|\.env\b|id_rsa|\.aws/credentials|\.netrc)", re.I)),
    ("system", "change own config", re.compile(r"(write|edit|append|overwrite)\b.{0,40}(settings\.json|CLAUDE\.md|AGENTS\.md|\.claude/hooks)", re.I)),
    ("tool-chain", "pipe to shell", re.compile(r"(curl|wget)[^\n|]{0,80}\|\s*(sh|bash|python3?)\b", re.I)),
    ("tool-chain", "decode and run", re.compile(r"base64\s+(-d|--decode)[^\n|]{0,40}\|\s*(sh|bash|python3?)\b", re.I)),
]

# A line that describes an attack, quotes one, or tells the agent to refuse it is not an instruction.
DEFENSIVE = re.compile(
    r"treat (it|this|that|them) as (data|text)|not (a|an) (command|directive|instruction)|"
    r"do not (follow|obey|execute|send)|never (follow|obey|send)|refuse|detect|flag|example|"
    r"pattern|attack|injection|untrusted|quoted|\bfor example\b|\bsuch as\b|\bcheck for\b",
    re.I,
)
SKIP = {".git", "node_modules", "build", "worktrees"}
URL = re.compile(r"https?://\S+")


def files(root: Path):
    for base in SCAN_DIRS:
        folder = root / base
        if not folder.is_dir():
            continue
        for p in folder.rglob("*"):
            if not p.is_file() or set(p.relative_to(root).parts) & SKIP:
                continue
            if p.suffix == ".md":
                yield p
    for name in SCAN_NAMES:
        p = root / name
        if p.is_file():
            yield p


def scan(root: Path):
    hits, excluded = [], 0
    for path in sorted(set(files(root))):
        for n, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            for group, label, rx in PATTERNS:
                if rx.search(line):
                    if DEFENSIVE.search(URL.sub("", line)):
                        excluded += 1
                    else:
                        excerpt = line.strip()[:120]
                        hits.append((path.relative_to(root).as_posix(), n, group, label, excerpt))
    return hits, excluded


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".")
    args = ap.parse_args(argv)
    root = Path(args.root).resolve()
    hits, excluded = scan(root)
    if hits:
        print("| File | Line | Group | Pattern | Excerpt |")
        print("|---|---|---|---|---|")
        for f, n, g, l, e in hits:
            print(f"| {f} | {n} | {g} | {l} | `{e}` |")
    print(f"\n{len(hits)} line(s) to review; {excluded} excluded as defensive or quoted.")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
