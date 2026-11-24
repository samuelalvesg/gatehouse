# 0001 - Item status follows the definition of done

**Status:** Example

## Context

A work item often has a checklist. Teams mark the item "done" when most boxes are ticked, or when someone stops discussing it. Both give a status that does not match what was delivered.

## Decision

1. A checklist does not split an item. An item with some boxes ticked and some open is one item, in progress.
2. The status is decided by the definition of done: all relevant subitems are complete. Never use a proportion. Twelve of sixty-two subitems is "in progress", not "20% done".
3. `Done` means delivered and checked, not "discussion stopped". Confirm it by reading the body, not from an old marker.
4. A subitem becomes its own item only when someone could plausibly pick it up alone. Otherwise it stays a checkbox.
5. Migrating an existing backlog is gradual and reviewed item by item. No script writes statuses in bulk. Automatic matching produces false positives, and automatic classification by a model disagrees with itself.

## Consequences

- The "done" view can be generated from the files, and it is trustworthy.
- Partial work stays visible in the backlog instead of disappearing.
- Some reviewer time goes into confirming items before they are marked done.
