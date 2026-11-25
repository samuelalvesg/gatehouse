---
name: generated-docs-freshness
description: Keep generated documentation and numbers in documents in sync with the code: generator scripts, a generated-file header, and a freshness gate that fails on stale generated files and on hand-typed counts. Use when changing a generated doc, a generator, or any number written in a document.
metadata:
  triggers:
    files:
      - 'scripts/docs/**'
      - 'docs/generated/**'
    keywords:
      - generated
      - freshness
      - gate
---

# Generated Docs and Freshness

## **Priority: P1 (HIGH)**

## What a freshness gate checks

- Each generated file equals a fresh run of its generator.
- Each generated file starts with a header that says it is generated.
- Canonical documents do not contain banned stale statements or hand-typed counts.
- Exit codes: 0 pass, 1 violations, 2 inputs missing. Exit 2 is "not verified", never a pass.

## Rules

1. **Never edit generated files by hand.** Change the generator and run it with its write flag.
2. **Numbers in prose come from a script** (test counts, document counts, totals), never typed by hand.
3. **A new generator** writes a header, produces deterministic output, and has a test that fails on a bad input.
4. **Run the gate before committing a documentation change.** Compare with the baseline: failures that already existed do not count, new ones do.
5. **Report exit 2 as not verified** and name the missing input.

## Workflow

1. Change the code or the generator.
2. Regenerate the affected files with their write flag.
3. Run the gate and read every line of output.
4. If a number in prose changed, recalculate it with a script and update the text.

## Anti-Patterns

- Typed counts of tests or documents.
- Suppression comments for current facts.
- Editing a generated file without its generator.
