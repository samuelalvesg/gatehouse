#!/usr/bin/env python3
"""Run `flutter analyze` in every Dart/Flutter package and group the issues by rule.

Read-only: it lists file:line:message per lint rule so a person can plan the
work. It never edits code. Use it to find every place a deprecated API still
appears across a monorepo, instead of running analyze package by package.

Usage:
  python3 scripts/lint/flutter_analyze_report.py [--root .] [--rule deprecated_member_use] [--out report.md]

Exit: 0 report written, 2 flutter not available (not verified).
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

SKIP = {".git", ".dart_tool", "build", "node_modules", ".claude", "worktrees", "target"}
RE_ISSUE = re.compile(
    r"^\s*(info|warning|error)\s+•\s+(.+?)\s+•\s+(.+?):(\d+):(\d+)\s+•\s+(\S+)\s*$"
)


def packages(root: Path):
    return sorted(
        p.parent for p in root.rglob("pubspec.yaml") if not (set(p.relative_to(root).parts[:-1]) & SKIP)
    )


def parse_analyze(text: str):
    """Return a list of dicts, one per issue line of `flutter analyze` output."""
    issues = []
    for line in text.splitlines():
        m = RE_ISSUE.match(line)
        if m:
            severity, message, file, row, col, rule = m.groups()
            issues.append(
                {"severity": severity, "message": message, "file": file, "line": int(row), "col": int(col), "rule": rule}
            )
    return issues


def analyze(package: Path, flutter: str):
    result = subprocess.run(
        [flutter, "analyze", "--no-pub"], cwd=package, capture_output=True, text=True, timeout=900
    )
    return parse_analyze(result.stdout)


def render(issues_by_package: dict, only_rule: str | None) -> str:
    by_rule = defaultdict(list)
    for package, issues in issues_by_package.items():
        for issue in issues:
            if only_rule is None or issue["rule"] == only_rule:
                by_rule[issue["rule"]].append((package, issue))
    lines = ["# Flutter analyze report", "", "Read-only: lists where each rule fires. Nothing was edited.", ""]
    lines += ["| Rule | Issues |", "|---|---|"]
    lines += [f"| `{rule}` | {len(items)} |" for rule, items in sorted(by_rule.items(), key=lambda kv: -len(kv[1]))]
    for rule, items in sorted(by_rule.items()):
        lines += ["", f"## `{rule}` ({len(items)})", ""]
        for package, issue in items:
            lines.append(f"- {package}/{issue['file']}:{issue['line']}:{issue['col']} {issue['message']}")
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".")
    ap.add_argument("--rule", help="only this lint rule")
    ap.add_argument("--out", type=Path, help="write the Markdown report here")
    args = ap.parse_args(argv)
    flutter = shutil.which("flutter")
    if not flutter:
        print("NOT VERIFIED: flutter is not on the PATH", file=sys.stderr)
        return 2
    root = Path(args.root).resolve()
    results = {}
    for package in packages(root):
        results[str(package.relative_to(root))] = analyze(package, flutter)
    report = render(results, args.rule)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(report, encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        sys.stdout.write(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
