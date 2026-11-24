---
name: backlog-items
description: Model and rules for a file-per-item backlog (one file per item, a Status field, an index table). Use when creating, finishing or changing the status of a backlog item.
---

# Backlog items

One item is one file under `docs/backlog/<epic>/<slug>.md`. Its metadata line holds the status. The index in `docs/BACKLOG.md` holds one row per open item, and each row repeats the status.

## Rules

- **Never move an item.** Finishing an item changes its status field. It does not cut the item and paste it elsewhere.
- **Done means 100%.** Mark `✅ Done` only when every checkbox is `- [x]`. Partial progress stays `🟡 Partial`. Never use a proportion.
- **The index is the open queue.** A done item does not appear in the index table.
- **Status and index agree.** The status in a row equals the status in the file.
- **Generated reports are never edited by hand.** Regenerate them with their script.
- **Do not re-classify on your own.** Triage proposes; the owner decides.

## Metadata line

```
> **Epic:** `core` · **ID:** `42` · **Status:** 🟡 Partial · **Registered:** 2026-01-01
```

## Procedure

1. Create an item: `python3 scripts/backlog/new_item.py --epic core --title "Short title"`.
2. Change its status: `python3 scripts/backlog/set_status.py <slug> --status "🟡 Partial"`. The script refuses `✅ Done` while checkboxes are open.
3. Check the result: `python3 scripts/backlog/check_backlog.py`. Exit 0 means clean.

If the scripts cannot run, edit both places by hand and say so as "not verified by script".
