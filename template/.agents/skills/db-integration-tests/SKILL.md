---
name: db-integration-tests
description: Choose and write backend tests: pure unit tests with mocks, controller contract tests, and database integration tests against a real database container, with a rule that skipped database tests fail the gate. Use when writing a test for a service, controller, repository or migration.
metadata:
  triggers:
    files:
      - '**/*Tests/**/*.cs'
      - '**/test/**/*.py'
    keywords:
      - integration test
      - Testcontainers
      - Skipped
      - regression
---

# Database Integration Tests

## **Priority: P0 (CRITICAL)**

## Choose the test type

| Behavior under test | Test type |
|---|---|
| Pure logic: validation, calculation, formatting | Unit test with mocked dependencies, no database |
| Controller routing and HTTP contract | Controller test with mocked services |
| Persisted rules, constraints, migrations, concurrency | Integration test against a real database container |

## Rules

1. **Unit tests never touch a database.** A test that needs a constraint or a query is an integration test.
2. **Integration tests reset their own data** before each test, so order does not matter.
3. **Skipped integration tests fail the gate.** If the container runtime is missing, the run must report the skip count, and a non-zero count is not a pass.
4. **Every change brings both levels** for its logic and its persisted path. A bug fix also brings a regression test that fails before the fix.
5. **Migrations are tested against existing rows.** An empty table hides a missing default on a non-nullable column.
6. **Do not weaken tests to pass.** No skipping, deleting or loosening an assertion to get green.

## Anti-Patterns

- Integration tests for pure logic.
- Shared state between integration tests.
- A green report with skipped integration tests.

## Related Topics

- Test strategy by layer: `test-strategy`.
- Migration review: `ef-core-migration-safety`.
