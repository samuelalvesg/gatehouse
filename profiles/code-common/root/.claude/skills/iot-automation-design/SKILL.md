---
name: iot-automation-design
description: Guides design and review of IoT/industrial automation data paths (Modbus, OPC UA, MQTT, gRPC, edge gateways, SCADA-like dashboards, rules/automation): timestamps and clocks, data quality, store-and-forward, sampling, ordering, security and safe commands. Use when touching collectors, protocols, ingestion, telemetry storage, alarms or automation rules.
---
# Data model
- Every sample carries: **source id, tag/point, value, quality, source timestamp, ingest timestamp, sequence/offset**. Never replace a missing/bad value with `0`; keep `quality` (good/uncertain/bad/stale) end to end, including the UI.
- Time: devices drift. Use monotonic clocks for intervals, UTC for wall time, record both source and ingest time, tolerate out-of-order and duplicate samples (dedupe by `(source, tag, ts, seq)`); document the clock-sync assumption (NTP/PTP).
- Units and scaling live in metadata, applied once at a documented boundary; keep the raw value if lossless debugging matters.

# Edge reliability
- **Store-and-forward**: persist locally first (WAL/SQLite/segment log), ack upstream only after durable write, replay in order after reconnect with idempotent keys; bounded disk with an explicit retention/overflow policy.
- Collector loops: per-device timeout, backoff + jitter, isolate one bad device from the rest (bulkhead), never block the poll loop on upstream I/O. See `resilience-patterns`.
- Back-pressure from cloud to edge must slow sampling or aggregate, not crash or grow memory.
- Report health as data: last-seen, error counters, queue depth, clock offset, firmware/version.

# Protocols
- **Modbus**: validate function/length/CRC, respect device timing and one-request-in-flight, batch contiguous registers, handle byte/word order explicitly, treat exceptions as quality=bad not crashes.
- **OPC UA**: prefer subscriptions + monitored items over polling, set publishing/sampling/queue sizes, handle session/subscription recovery and certificate trust explicitly (no trust-all in production).
- **MQTT**: choose QoS per data class, retained/LWT for presence, topic namespace + versioning, bounded payload, auth + TLS, dedupe at the consumer (QoS 1 duplicates).
- **gRPC/streams**: deadlines, keepalive, flow control, max message size, versioned `.proto` (additive changes).
- Validate **all** external bytes at the edge (length, range, enum); fuzz decoders (`fault-injection-testing`).

# Automation / commands
- Reads are safe; **writes/commands are not**: declare effect, require authorization, idempotency key, confirmation/state check, timeout and an audit trail; an interlock/safety function never depends on this software path alone.
- Rules/alarms: hysteresis/deadband, debounce, rate-limit notifications, state machine with explicit states, evaluation on quality-aware values, test with replayed traces.
- Deterministic simulation: ship a simulator/replay of device traces so tests never need real plants; real customer data never enters fixtures.

# Performance
Batch writes, columnar/time-partitioned storage for telemetry, downsample for display, cap cardinality, avoid per-sample allocation on the hot path; measure with `performance-profiling`.

# Output (≤15 lines)
`PATH | data/quality/time handling | durability | protocol risks | command safety | tests/replay`.

## Related skills
- `fault-injection-testing`: replay and fault tests for the data path.
- `performance-profiling`: measure the ingestion path.
- `resilience-patterns`: store-and-forward and reconnect rules.
