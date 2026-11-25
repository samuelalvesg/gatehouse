---
name: test-mutation-audit
description: Evaluates test suite quality and coverage by introducing artificial faults (mutations) to verify that tests fail when code is defective.
---
# Mutation Types
1. **Conditional Mutations**: Invert comparison operators (`>` to `<=`, `==` to `!=`).
2. **Boundary Mutations**: Offset loop boundaries and thresholds (`< n` to `<= n`, `offset + 1`).
3. **Return Value Mutations**: Replace return values with default/null/empty collections.
4. **Statement Removal**: Comment out key side effects or cache updates to ensure tests verify state changes.

# Audit Workflow
1. Identify high-risk or core business logic files.
2. Introduce candidate mutations (manual or via tooling if present in repo).
3. Execute relevant test suites.
4. If tests pass despite the mutation, the mutation **survived**:
   - Flag as inadequate test assertion or missing scenario.
5. If tests fail, the mutation was **killed** (effective test).

# Output (<= 25 lines)
`# | mutated location | mutation applied | test result (killed/survived) | required test coverage improvement`

# Additional guidance
- Fixed baseline: SHA, exact command, toolchain, host, selected tests; an old run is valid only for its SHA. A required test is discovered **once**; a missing test or missing report **must not** be green.
- Typical false greens: assertion that repeats the mock · stale fixture that breaks before the tested behavior · subprocess/checker with a swallowed error · a test that never runs (silent skip, `Skipped` > 0) · assertion without `await`.
- Mutate only in a disposable copy/branch (invert a condition, drop an `if`, wrong return value, inject I/O failure); the suite must fail. Fixtures: check against current contract/protocol/version; sweep the whole fixture family; keep intentionally malformed ones. Efficiency without losing the gate: remove duplicate setup before reducing coverage; preserve cancellation, cleanup failure, permission, capacity, identity and concurrency cases; live tests never come from cache.
- Forbidden: suppressing a failure, blind retry, raising a timeout or deleting a distinct assertion just to go green; changing the gate without showing it still detects failure. A failure on `main` may be pre-existing: attribute by executed SHA and clean baseline. Backend: confirm "Skipped: 0". Output ≤15 lines: `TARGET | MUTAÇÃO | REPROVOU? | CONSEQUÊNCIA | CORREÇÃO`.
