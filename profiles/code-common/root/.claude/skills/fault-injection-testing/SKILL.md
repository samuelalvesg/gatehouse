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
- Real databases/brokers for integration (Testcontainers); no mocking of what you are testing. Report `Skipped: 0`.
- Chaos/DAST/fuzz only in local or ephemeral environments, never against production or third parties.
- Real customer data never in fixtures.

# Output (≤15 lines)
`RISK | technique | test | failure injected | assertion | tool`.
