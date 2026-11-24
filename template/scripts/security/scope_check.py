#!/usr/bin/env python3
"""Check a testing scope file before any active test runs. Standard library only.

The scope file is JSON, written by the person who owns the system:

  {
    "owner": "Team name",
    "authorized_by": "Name and role of the person who approved the test",
    "environment": "staging",
    "valid_from": "2026-11-01",
    "valid_until": "2026-11-30",
    "allowed_hosts": ["staging.example.test"],
    "allow_production": false
  }

Exit: 0 the target is in scope today, 1 out of scope or expired, 2 scope file invalid.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

REQUIRED = ("owner", "authorized_by", "environment", "valid_from", "valid_until", "allowed_hosts")


def check(scope: dict, target: str, today: date) -> list[str]:
    """Return the reasons the target is out of scope. An empty list means in scope."""
    missing = [k for k in REQUIRED if not scope.get(k)]
    if missing:
        raise ValueError("missing fields: " + ", ".join(missing))
    reasons = []
    if not (date.fromisoformat(scope["valid_from"]) <= today <= date.fromisoformat(scope["valid_until"])):
        reasons.append("outside the authorized period")
    if scope["environment"] == "production" and not scope.get("allow_production", False):
        reasons.append("production is not authorized")
    host = urlparse(target if "://" in target else f"//{target}").hostname or ""
    if host not in set(scope["allowed_hosts"]):
        reasons.append(f"host {host or '(none)'} is not in allowed_hosts")
    return reasons


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("scope_file", type=Path)
    ap.add_argument("target")
    ap.add_argument("--today", type=date.fromisoformat, default=date.today(), help="for testing only")
    args = ap.parse_args(argv)
    try:
        scope = json.loads(args.scope_file.read_text(encoding="utf-8"))
        reasons = check(scope, args.target, args.today)
    except (OSError, ValueError, KeyError) as err:
        print(f"INVALID SCOPE: {err}", file=sys.stderr)
        return 2
    if reasons:
        print("OUT OF SCOPE: " + "; ".join(reasons))
        return 1
    print(f"IN SCOPE: {args.target} until {scope['valid_until']} ({scope['environment']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
