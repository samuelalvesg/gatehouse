---
name: test-strategy
description: Defines test coverage plans, test level distribution (unit, integration, contract, E2E), edge cases, and regression test suites for new features and bug fixes.
---
# Testing Pyramid & Allocation
1. **Unit Tests (Fast, Isolated, Deterministic)**:
   - High volume (~70%). Cover pure business domain logic, calculation rules, edge cases, and state machines without I/O or network.
2. **Integration Tests (Subsystems & Real Dependencies)**:
   - Medium volume (~20%). Cover repository queries, database migrations, API routes, middleware, and serialized communication.
3. **Contract / E2E Tests (System Boundaries)**:
   - Focused volume (~10%). Cover critical user journeys, external webhook contracts, and end-to-end integration flows.

# Test Strategy Checklist
- Given/When/Then scenario coverage.
- Happy path, boundary values (empty, zero, max), negative/unauthorized paths.
- Concurrency and race conditions where state is shared.
- Idempotency of retries and network reconnects.
- Clear test names following standard convention: `UnitOfWork_StateUnderTest_ExpectedBehavior`.

# Output
Test plan with prioritized test cases, expected inputs/outputs, and target file locations.

# Additional guidance
- Repo rule: every change brings **unit + integration**; a bug brings a **regression** test; reuse existing helpers.
- Layers: domain rule/service → unit test (mock at the edge); route/contract → HTTP integration test; persistence/tenant/migration → database test against a real database with at least one pre-existing row; UI state → widget test covering loading, empty, error, offline and ok; native code or app launch → integration test on a real device or desktop target.
- Find existing tests: `grep -rn "<symbol>" <test dirs>`. Test name = scenario id + English description. No skipped tests are allowed.
- Flutter mocks: use `mocktail`; never `any()` (use typed matchers); shared mocks live in `test/shared/`, with no local copies. Test names: `Method_Scenario_ExpectedBehavior`. No `Future.delayed` sleeps: use `pumpAndSettle()` or a condition.
- Output ≤15 lines: `SCENARIO | LAYER | TEST (existe/falta) | RISK`.

# Project rules
- Every change brings unit and integration tests; a bug fix brings a regression test.
- Reuse existing test helpers. Before writing one, search the test folders for the symbol.
- Name tests with the scenario and the expected behaviour, in the project's naming convention.

# Known pitfalls
- Tests that look for on-screen text break on renames: prefer keys or widget types.
- A test that only passes proves nothing: prove it by mutation (restore the old code and watch it fail). Do the same for security guards.
- Failures caused by the environment (missing native libraries, missing browser driver, wrong tool version) are not regressions: record them as not verified, with the reason.
