---
name: backlog-triage
description: Read a file-per-item backlog and report facts about it (open and done items, contradictions, empty bodies) without editing anything. Use before planning work from the backlog or when auditing its state.
---

# Backlog triage

Triage reads the backlog and reports. It never edits an item, never changes a status and never classifies an item by model.

## Procedure

1. Run `python3 scripts/backlog/triage_backlog.py --tsv scripts/out/backlog_triage.tsv`.
2. Read the summary: item count and the count of each flag.
3. Open the TSV and look at the flagged rows.

## Flags

- `done-with-open-items`: the status says done, but the body still has an open checkbox. Either the status is wrong or the checkbox is stale. Decide with the owner; do not pick one yourself.
- `state-in-title`: the title carries state such as `[x]`, `~~` or "DONE". Titles name work; state belongs in the status field.
- `empty-body`: nothing after the metadata line. Either the body was cut or the item was never written.

## Rules

- Every flag is a text match. If someone disputes one, open the file and check the line.
- A count that depends on a model's judgement is not a fact. Leave it out of the report.
- Owners are decided by the people who run the project, not by keyword rules.
