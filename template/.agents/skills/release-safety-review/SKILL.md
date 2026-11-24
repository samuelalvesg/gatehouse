---
name: release-safety-review
description: Review of how a change is rolled out and reversed (schema migrations, feature flags, blue-green, canary and rolling deploys, rollback, health checks, backup and restore evidence, disaster recovery). Use before a release or when a change touches migrations, configuration or infrastructure.
---

# Release safety review

A change is safe when it can be reverted without data loss and deployed without an outage. Check both before the release, not after the incident.

## Checklist

- **R1 Expand and contract.** A schema change is split into steps that each work with both the old and the new code: add the column or table, backfill, switch reads and writes, then remove. A single step that drops or renames breaks the running version.
- **R2 Migration locks.** Large table changes are checked for lock time on the production size, or run in batches. Not verified if no production-size data was tested.
- **R3 Backfill.** A backfill is idempotent, resumable, rate-limited, and checked by a count or checksum afterwards.
- **R4 Feature flags.** A risky behaviour sits behind a flag with an owner, a default that is safe, and a removal date. Turning it off restores the old behaviour without a deploy.
- **R5 Deploy strategy.** The chosen strategy (rolling, blue-green, canary) is stated, with the signal that stops it (error rate, latency, a business metric).
- **R6 Rollback.** There is a written rollback: the previous artifact, the flag to turn off, and whether a migration must be reversed or only fixed forward. A migration that cannot be reversed says so in the plan.
- **R7 Health checks.** Liveness and readiness are separate. Readiness fails while the service cannot serve, so traffic is not sent to it during start-up or shutdown.
- **R8 Shutdown.** In-flight requests and queue messages finish or return to the queue on shutdown.
- **R9 Backups.** Backups run, are encrypted, and have been restored at least once. Without evidence this is `NOT VERIFIED`, and the release says so.
- **R10 Disaster recovery.** The recovery time and recovery point objectives are written down for the data that matters, with the steps to meet them.
- **R11 Configuration.** Environment-specific values are not hard-coded. A missing value fails at start-up, not at the first request.
- **R12 Observability.** The release names the new metrics or logs that will show whether it worked, and who watches them.

## Related skills

Pre-release gate and version checks: `release-checklist`. Failure isolation: `resilience-patterns`. Signals to watch: `telemetry-tracing`. Data changes under concurrency: `data-consistency-review`.

## Output

One table, the same format as `web-app-security-audit`: ID, check, status (`PASS`, `FAIL`, `N/A`, `NOT VERIFIED`), severity, evidence (`file:line`), fix. Then the fixes for every `FAIL` with `CRITICAL` or `HIGH` severity. Anything that needs a running system (load test, restore drill, production traffic) is `NOT VERIFIED` unless evidence is attached.

