---
name: reuse-before-create
description: Check for an existing helper, widget, service or document before creating a new one, and unify duplicates instead of adding a second copy. Use before writing any new function, class, screen, component or document in a repository that already has code.
---

# Reuse before create

Every new helper is a future duplicate unless someone looks first. Look before you write.

## Procedure

1. **Search by name and by behaviour.** Grep for the verb and the noun (for example `format date`, `parse phone`, `empty state`). Search the shared folders (`utils`, `common`, `shared`, `widgets`, `services`) before the feature folder.
2. **Search the diff.** Run `python3 scripts/lint/detect_duplicates.py --root <changed folder> --window 8` on the files you touched. A repeated block is a candidate to reuse or unify.
3. **Decide.**
   - An existing helper does the job: reuse it. If it is almost right, extend it with a parameter rather than copy it.
   - Two copies already exist: unify them in one change, with tests, before adding a third.
   - Nothing exists: create it in the shared folder that the rest of the code would search first, and say where in the report.
4. **Report.** Name the helper you reused, or the search you ran and found nothing, so the reviewer can check.

## Rules

- A new copy of a function that already exists is a defect, not a style choice. Reviewers reject it.
- Do not reuse by importing a feature's private code into another feature. Move the shared part to a shared place first.
- Searching is not optional for a duplicate-looking name: `formatDate` and `format_date` in two languages are still the same job.
