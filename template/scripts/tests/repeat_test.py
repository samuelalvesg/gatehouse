#!/usr/bin/env python3
"""Run a test command N times and report the pass rate. Standard library only.

A test that both passes and fails with the same code is flaky. A test that always fails is a
real failure. Use this before blaming a flaky test on the environment.

Usage:
  python3 scripts/tests/repeat_test.py --runs 10 -- python3 -m unittest test_module

Exit: 0 every run passed, 1 at least one run failed.
"""

from __future__ import annotations

import argparse
import subprocess
import sys


def run(cmd: list[str], runs: int) -> list[bool]:
    return [subprocess.run(cmd, capture_output=True, text=True).returncode == 0 for _ in range(runs)]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--runs", type=int, default=5)
    ap.add_argument("command", nargs=argparse.REMAINDER)
    args = ap.parse_args(argv)
    cmd = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not cmd or args.runs < 1:
        print("usage: repeat_test.py --runs N -- <command>", file=sys.stderr)
        return 2
    results = run(cmd, args.runs)
    passed = sum(results)
    print(f"{passed}/{args.runs} passed")
    if passed == args.runs:
        return 0
    if passed == 0:
        print("always failing: a real failure, not flakiness")
    else:
        print("flaky: the same command passed and failed")
    return 1


if __name__ == "__main__":
    sys.exit(main())
