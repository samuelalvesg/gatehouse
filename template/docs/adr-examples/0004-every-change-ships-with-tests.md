# 0004 - Every change ships with tests

**Status:** Example

## Context

Changes merged without tests broke behaviour that nobody noticed until release. Reviewers could not tell whether a change worked, only that it looked right.

## Decision

1. Every new or changed implementation comes in the same pull request with unit tests for the logic and integration tests for the full path.
2. A bug fix comes with a regression test that fails before the fix and passes after.
3. Reuse the existing test helpers before writing new ones.
4. The exception is a change with no testable behaviour: documentation only, or a mechanical rename. The pull request says which case applies. "Hard to test" is not an exception; it is a reason to isolate the code behind a contract.
5. Tests follow the same language rule as the code.

## Consequences

- Pull requests are larger, and reviewers can rely on the tests.
- Regressions fail in CI, not in production.
- Slow test suites need their own work; they are not a reason to skip tests.
