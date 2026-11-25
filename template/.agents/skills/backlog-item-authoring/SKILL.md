---
name: backlog-item-authoring
description: Write and update backlog items as one file per item, with a metadata line, a status set by the Definition of Done, a spec section, and the rule that a finished item never moves. Use when registering an item, changing its status, or writing a spec inside a backlog file.
metadata:
  triggers:
    files:
      - 'docs/backlog/**/*.md'
      - 'docs/BACKLOG.md'
    keywords:
      - Status
      - Definition of Done
      - Spec
---

# Backlog Item Authoring

## **Priority: P0 (CRITICAL)**

## Rules

1. **One file per item**, inside the folder of its epic. Do not create an epic for a single item.
2. **Metadata line** right under the title, as a blockquote with epic, id, status and registration date.
3. **Status follows the Definition of Done.** An item is done only when no relevant checklist item is left open and the delivery can be verified in the body. Never use a percentage or a count of checkboxes. A mixed checklist stays in one file.
4. **The body never moves.** Closing an item changes the status field only. Do not cut the body into a "done" file.
5. **Indexes are generated.** Never edit a generated index or report by hand. Items missing from the index stay in their epic folder until the index is regenerated.
6. **Spec section** uses `SHALL` for requirements and `WHEN/THEN` for scenarios.
7. **Identity is the pair (epic, id).** Cross-references resolve inside the same epic; a reference to a missing id stays as plain text.

## Workflow

1. Search for an existing item first and extend it instead of duplicating it.
2. Create the file with the metadata line, then the sections: problem, open decisions, done criteria, references.
3. Mark undecided points as undecided. Do not invent a decision.
4. Change the status only after re-reading the body against its checklist.

## Anti-Patterns

- No status taken from a checkbox count.
- No copy of a finished body into another file.
- No hand edit of a generated index.
- No item without a metadata line.
