---
name: data-consistency-review
description: Review of how a change keeps data correct under concurrency, retries and partial failure (idempotency, locking, check-then-act, sagas, outbox, dead-letter queues, eventual consistency). Use when a change writes state from several steps, handles events or webhooks, or moves money, quota or stock.
---

# Data consistency review

Read the write path end to end: request, transaction boundary, external calls, events, retries. Assume every step can run twice and every call can fail after it succeeded.

## Checklist

- **C1 Idempotency.** Every write triggered by a retry, webhook or queue message has an idempotency key or a natural unique key, stored with a unique constraint. A repeat returns the first result.
- **C2 Concurrent updates.** Read-modify-write on shared state uses a transaction, a conditional update (`WHERE version = ?`), or a pessimistic lock. Name the lock and its scope.
- **C3 Check-then-act.** No separate read decides a write without the database enforcing the same rule (unique index, check constraint, conditional update).
- **C4 Distributed locks.** A lock held across a network call has a lease or timeout, and the code still works if the lock expires mid-operation.
- **C5 Multi-step operations.** A saga or compensation exists for each step that can fail after an earlier step committed, or the steps run in one transaction.
- **C6 Outbox.** An event is written in the same transaction as the state change, or the change is documented as at-most-once.
- **C7 Dead letters.** A message that keeps failing moves to a dead-letter store with the reason, and someone is alerted. It does not loop forever.
- **C8 Eventual consistency.** Each read that follows a write states whether it may be stale, and the UI or API handles that (no "I just saved it and it is gone").
- **C9 Ordering.** Code that depends on message order handles out-of-order delivery, or the broker guarantee is written down.
- **C10 Partitioned or replicated reads.** A read right after a write goes to the primary, or it tolerates lag.
- **C12 Cache keys.** Every cached value that depends on the user, tenant or role has that identity in its key. A shared key that serves one user's data to another is a FAIL with severity CRITICAL.
- **C13 Cache invalidation.** Each write that changes a cached value invalidates or updates it, or the cache has a short expiry stated in the change. Data read from a cache is never the only source for a money, permission or quota decision.
- **C11 Money and quotas.** Decrements never go negative under concurrency, and a failed external charge is reconciled, not assumed.

## Related skills

Retries, timeouts and circuit breakers: `resilience-patterns`. Query plans and missing indexes: `query-performance-tuner`. Browser and API input checks: `web-app-security-audit`.

## Output

One table, the same format as `web-app-security-audit`: ID, check, status (`PASS`, `FAIL`, `N/A`, `NOT VERIFIED`), severity, evidence (`file:line`), fix. Then the fixes for every `FAIL` with `CRITICAL` or `HIGH` severity. Anything that needs a running system (load test, restore drill, production traffic) is `NOT VERIFIED` unless evidence is attached.

