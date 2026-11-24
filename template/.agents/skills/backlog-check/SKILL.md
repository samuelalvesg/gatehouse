---
name: backlog-check
description: Run the backlog integrity checks (index and item agreement, orphans, done rules) as a gate before finishing a change that touches backlog files.
---

# Backlog check

Run this gate before you finish any change to `docs/BACKLOG.md` or `docs/backlog/`.

## Procedure

```bash
python3 scripts/backlog/check_backlog.py --verbose
python3 -m unittest discover -s scripts/backlog
```

## What the checks cover

| Check | Meaning |
|---|---|
| C1 | every item file has a metadata line |
| C2 | the epic in the metadata matches its folder |
| C3 | the status is one of the allowed statuses |
| C4 | every index row points to an existing file |
| C5 | every item file is listed in the index |
| C6 | the status in the index equals the status in the file |
| C7 | no done item is listed in the index |
| C8 | no done item has an open checkbox |

## Reporting

- Exit 0: report the item count and "clean".
- Exit 1: list each violation with its check code. Fix the item or the index, then run again.
- If the checks cannot run, write `NOT EXECUTED: <reason>` in the report. Never write "clean" without running them.
