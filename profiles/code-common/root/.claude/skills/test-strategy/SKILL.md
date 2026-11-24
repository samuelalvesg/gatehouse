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
- Layers: domain rule/service → xUnit (mock at the edge); route/contract → HTTP integration (`WebApplicationFactory`: happy, 4xx, authz/tenant); persistence/tenant/migration → `[DatabaseFact]` + Testcontainers with ≥1 pre-existing row; Flutter widget/state → `flutter test` with the 5 states (loading/empty/error/offline/ok); Rust → `#[cfg(test)]` + `tests/` (invariant + I/O error); app opens/native code → `integration_test` + `flutter drive` (web, Android) or `flutter test -d linux` (cold start + Rust core responds + 1 check per risky plugin).
- Find existing tests: `grep -rn "<symbol>" <test dirs>`. Test name = scenario id + English description. Backend requires "Skipped: 0".
- Known Flutter pitfalls: tests that look for **screen text** age (a renamed button fails a good baseline): prefer a key or widget type. Web: `flutter drive` needs the `chromedriver` of the same Chrome; in a container, `--no-sandbox`. Tests using native Rust need the compiled library (the Linux build produces it); without it `setUpAll` fails on the native library — environmental, not a regression. Rust on web: after rebuilding `web/pkg`, `wasm-opt` must be **117** (apt's 108 broke the `__wbindgen_externrefs` export); check the export and run the minimal core-init test in Chrome. A test that only passes proves nothing: **prove by mutation** (restore the old code and watch it fail); security guards too.
- Output ≤15 lines: `SCENARIO | LAYER | TEST (existe/falta) | RISK`.
