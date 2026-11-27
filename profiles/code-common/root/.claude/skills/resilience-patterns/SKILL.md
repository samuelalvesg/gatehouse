---
name: resilience-patterns
description: Designs and reviews resilience for services, workers, edge gateways and offline-first apps: timeouts, retries with jitter, circuit breakers, bulkheads, backpressure, idempotency, graceful degradation, recovery. Use when adding an external call, queue, reconnect loop, sync, or when a failure mode is unclear.
---
# Principle
Assume every dependency (network, broker, DB, device, clock) fails, slows down or lies. Failure behavior is part of the contract: define it **before** the happy path ships, and prove it with a test (`fault-injection-testing`).

# Checklist (per external call or loop)
1. **Deadline**: every call has a total timeout (and idle timeout for streams); propagate cancellation (`CancellationToken` in C#, `select!`/drop on cancel in Rust, cancel subscription in Dart). No unbounded wait.
2. **Retry** only idempotent or keyed operations; exponential backoff **with jitter**, capped attempts and total budget; never retry 4xx/validation; respect `Retry-After`. Retries multiply load: bound them per client, not per call.
3. **Circuit breaker** on repeated failure: fail fast, half-open probe, visible state (metric + log). Fallback decided per call: cached value, degraded response, or explicit error; never a silent wrong answer.
4. **Bulkhead**: separate pools/queues/concurrency limits per dependency so one slow dependency cannot starve the rest.
5. **Backpressure**: bounded queues/channels; define the overflow policy (block, drop oldest/newest, shed load) per data class; never an unbounded buffer.
6. **Idempotency**: stable keys for writes, at-least-once delivery + dedupe at the consumer (outbox/inbox), commutative or versioned updates for sync (CRDT/last-writer rules written down).
7. **Reconnect**: backoff + jitter, re-subscribe, resync state after reconnect, detect half-open connections (heartbeat/keepalive), bounded memory while offline.
8. **Startup/shutdown**: readiness vs liveness, dependency-optional startup, graceful drain (finish in-flight, flush buffers), crash-safe on-disk writes (write temp + atomic rename / WAL).
9. **Data safety**: no partial writes visible; migrations reversible or two-phase; backups restorable (restore tested, not assumed).
10. **Observability of failure**: error, retry count, breaker state, queue depth and lag are metrics with alerts (`telemetry-tracing`).

# Anti-patterns
Retry storms · retry inside retry · catch-all that swallows errors · infinite loop without sleep/backoff · shared mutable state across reconnects · timeouts longer than the caller's own deadline · "works on my LAN" assumptions (latency, MTU, clock skew).

# Per stack
- **C#**: `Microsoft.Extensions.Resilience`/Polly v8 pipelines (timeout → retry → breaker → bulkhead order matters), `HttpClient` via `IHttpClientFactory`, `CancellationToken` everywhere, outbox for events.
- **Rust**: `tokio::time::timeout`, bounded `mpsc`, `CancellationToken`/graceful-shutdown signal, no lock across `.await`, `tower` layers (timeout/retry/limit) where applicable, crash-safe writes.
- **Dart/Flutter**: `Stream` subscriptions cancelled in `dispose`, retry with backoff in the data layer (not in widgets), offline queue persisted, UI shows offline/stale state.

## Example

Input (illustrative): `WeatherClient.Get()` calls an external API with no timeout.

| DEPENDENCY | Failure mode | Timeout | Retry | Breaker/fallback | Backpressure | Idempotency | Test |
|---|---|---|---|---|---|---|---|
| weather API | call hangs | none → 3 s total | none → 2 attempts with jitter (GET is idempotent) | serve last cached value, marked stale | n/a | GET | fault injection: 30 s delay, assert return within 3 s |

# Output (≤15 lines)
`DEPENDENCY | failure mode | timeout | retry | breaker/fallback | backpressure | idempotency | test`.

## Related skills
- `fault-injection-testing`: prove the failure behaviour with injected faults.
- `telemetry-tracing`: metrics and alerts for retries, breakers and queue depth.
