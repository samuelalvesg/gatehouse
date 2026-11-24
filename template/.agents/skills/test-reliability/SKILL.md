---
name: test-reliability
description: Decide whether a failing or skipped test is a real problem, a flaky test, or a skip that hides a gap. Use when a test fails once and passes on rerun, when a suite reports skipped tests, or before marking a test as ignored.
---

# Test reliability

A green run with skipped tests is not a full pass. A failure that goes away on rerun is not a fix. Classify before you act.

## Procedure

1. **Reproduce.** Run the failing test alone, then repeat it: `python3 scripts/tests/repeat_test.py --runs 10 -- <command>`.
   - Always fails: a real failure. Find the cause (`root-cause-debug`) before any change.
   - Passes and fails with the same code: flaky. Record it; do not call it fixed.
2. **Find the source of the flakiness.** Shared state between tests, the clock, the network, test order, ports, parallel writes to one database. Name the source in the report.
3. **Skips.** Run `python3 scripts/tests/check_skipped.py --file <log> --allow 0` on every suite. A skip needs a reason in the code and an owner. A skipped test that depends on infrastructure is `NOT VERIFIED` until the infrastructure runs.
4. **Quarantine only with an expiry.** A flaky test may be moved out of the required set, but only with a date to come back and an owner. After the date, it fails the build again.

## Rules

- Never weaken an assertion, delete a test, or add a retry loop to make a test pass. A retry hides the bug.
- A flaky test is a backlog item with its source named, not a note in a chat.
- A test that depends on time is fixed with an injected clock, not with a longer timeout.
- Report every run count. "Passed once" is not evidence.
