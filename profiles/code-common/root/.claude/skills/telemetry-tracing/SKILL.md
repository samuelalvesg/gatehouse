---
name: telemetry-tracing
description: Structured logs, health metrics and distributed tracing (OpenTelemetry) without degrading performance or leaking data. Use when instrumenting a service, queue, ingestion path or critical endpoint.
---
# Basis
Reuse the project's existing OpenTelemetry setup (check: `grep -rn "AddOpenTelemetry" .`); do not add another log/trace library without approval.

# Logs (12-Factor XI: stream to stdout)
- `ILogger<T>` with a **template**, never interpolation: `_log.LogInformation("Slot {SlotId} assigned to {UserId}", id, uid)`.
- Levels: `Error` = action needed; `Warning` = degraded/recoverable; `Information` = business milestone; `Debug` = diagnostics (off in prod).
- Correlation properties: `TraceId`, `TenantId`, `UserId` (id, not e-mail). **Never** log: password, token, key, PII, whole request body, card data.
- Hot path: `[LoggerMessage]` source generator or an `IsEnabled` guard; no per-item log inside an ingestion loop (aggregate: 1 log per batch).
- Exceptions: `LogError(ex, "msg {Ctx}", ctx)` once, at the boundary; do not log-and-rethrow at every layer.

# Metrics (RED + saturation)
- RED per endpoint/consumer: **R**ate, **E**rrors, **D**uration (histogram, not average).
- Saturation: pending queue/outbox, pool connections, ingestion lag, memory.
- Via `System.Diagnostics.Metrics` (`Meter`, `Counter`, `Histogram`) collected by OTel.
- Cardinality: **low**-cardinality tags (route, status, tenant only if few); never user/entity ids as tags.
- Naming: `<app>.<module>.<measure>` + unit.

# Tracing
- One `ActivitySource` per module; `StartActivity("module.operation")` only at boundaries (I/O, external call, message/realtime handler); not in pure methods.
- Propagate context (W3C `traceparent`) over HTTP, messages and gRPC; include `TraceId` in error responses (helps support).
- Attributes: `tenant.id`, `db.system`, result. No personal data.
- Sampling: head-based (e.g. 10%) in production; 100% on error. Low-value spans are not created.

# Health
`/health/live` (process alive, no dependencies) and `/health/ready` (database, queue). Readiness must not fail the pod for an optional dependency.

# Cost (measure it)
Instrumentation must not double latency: compare p95 before/after on the hot path; spans can be switched off by config (12-Factor III) without redeploy.

# Checklist
- [ ] Structured template, no interpolation
- [ ] No secret/PII in log, tag or span
- [ ] RED metric + saturation for the component
- [ ] Context propagated between services
- [ ] Cardinality checked
- [ ] Overhead measured (or "not measured")
- [ ] Test: log/metric emitted on the error path

## Workflow

1. Find the existing OpenTelemetry setup (`grep -rn "AddOpenTelemetry" .`) and reuse it.
2. List the component's boundaries: inbound requests, consumers, external calls, saturation points.
3. Add one log template, one RED metric or saturation gauge, and one span per boundary.
4. Check for personal data and high-cardinality tags before merging.
5. Measure overhead on the hot path against the budget; write "not measured" if there is no benchmark.
6. Fill the checklist and the output table.

# Output (≤15 lines)
`COMPONENT | logs | metrics | spans | overhead | pending`.
