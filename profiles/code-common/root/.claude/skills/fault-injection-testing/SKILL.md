---
name: fault-injection-testing
description: Test strategies beyond the happy path: fault injection, property-based tests, fuzzing, deterministic time/clock, contract tests, replay/soak/chaos for services, edge gateways and offline-first apps. Use when writing tests for resilience, protocols, parsers, sync, concurrency or timing-dependent code.
---
# Goal
Prove behavior under failure, not just correctness on valid input. A test that cannot fail when the code is wrong proves nothing (`test-mutation-audit`).

# Techniques (pick by risk)
| Technique | Use for | Tools |
|---|---|---|
| **Fault injection** | timeouts, disconnects, partial writes, slow/duplicate/out-of-order messages, DB/broker down | fake transport/clock, Toxiproxy, Testcontainers stop/pause, `tower`/Polly test hooks, failing `Stream`/`HttpClient` handlers |
| **Property-based** | parsers, codecs, state machines, merge/CRDT, round-trips, invariants | `FsCheck` (C#), `proptest`/`quickcheck` (Rust), `glados`/`kiri_check` (Dart) |
| **Fuzzing** | binary/protocol decoders, untrusted input | `cargo fuzz`/`libFuzzer`, `SharpFuzz`; keep a corpus + crashers as regression tests |
| **Deterministic time** | retries, timers, rate limits, expiry | injected clock (`TimeProvider`, `tokio::time::pause`, `fake_async`); never `sleep` in tests |
| **Concurrency** | races, deadlocks, ordering | `loom` (Rust lock-free), stress loops with seeds, `Task` scheduling control; assert invariants, not timing |
| **Contract tests** | API/proto/MQTT payload compatibility across versions | schema/golden files, consumer-driven tests, `buf breaking` for protobuf |
| **Replay/simulation** | IoT/automation logic, alarms, rules | recorded or synthetic traces, device simulators; assert state/outputs, not logs |
| **Soak/chaos** | leaks, drift, recovery | long-run test with metrics assertions; kill/restart/network-partition in a disposable environment only |
| **Golden/widget** | Flutter UI states | widget tests for 5 states, golden images only for stable components |

# Rules
- Every resilience claim (retry, breaker, dedupe, store-and-forward) has a test that **injects the failure** and asserts the outcome (no loss, no duplicate, bounded memory, recovers within N s).
- Seeds are printed and reproducible; flaky = bug (in test or code), never "retry the CI".
- Real databases/brokers for integration (Testcontainers); no mocking of what you are testing. Report the number of skipped tests; for database tests it must be zero.
- Chaos/DAST/fuzz only in local or ephemeral environments, never against production or third parties.
- Real customer data never in fixtures.

## Workflow

1. Name the resilience claim to test (for example, "a retry does not duplicate a write").
2. Pick the technique from the table by risk.
3. Inject the failure at the boundary: fake transport, stopped container, failing handler.
4. Confirm the test fails when the guard is removed (see Rules).
5. Assert the outcome: no loss, no duplicate, bounded memory, recovery within N seconds.
6. Record the seed and the failure injected in the output table.

## Example

Input (illustrative): `PaymentClient.Charge` retries after a timeout.

Test: the fake handler times out on the first call and succeeds on the second. Assert one charge is recorded and the idempotency key is the same on both calls.

| RISK | Technique | Test | Failure injected | Assertion | Tool |
|---|---|---|---|---|---|
| high | fault injection | `PaymentClientRetryTest` | timeout, then success | one record, same key | fake `HttpMessageHandler` |

# Output (≤15 lines)
`RISK | technique | test | failure injected | assertion | tool`.

## Related skills
- `test-mutation-audit`: check that the fault tests can actually fail.
