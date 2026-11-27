---
name: api-change-review
description: Review of a change to a public or cross-team API (HTTP, gRPC, events, webhooks): compatibility, versioning, deprecation, delivery guarantees and limits at the boundary. Use when a change alters a request, response, event schema or webhook payload.
---

# API change review

Decide who is affected before reading the diff: mobile apps that cannot be updated, partners, other services, and webhook receivers.

## Checklist

- **V1 Compatibility.** Existing clients keep working. Removing or renaming a field, changing its type or meaning, or making an optional field required is a breaking change.
- **V2 Versioning.** A breaking change ships under a new version (path, header or schema version). The old version keeps working for a stated period.
- **V3 Deprecation.** The old behaviour is marked deprecated in the contract, with a date and a replacement. Usage is measured before removal.
- **V4 Unknown fields.** Clients that receive an extra field do not fail. Servers ignore unknown input fields, or reject them on purpose and say so.
- **V5 Defaults.** A new default value does not change the result for clients that did not ask for it.
- **V6 Webhooks.** Delivery is at least once. The payload carries an event ID, the receiver is told to deduplicate, and the signature is documented (the signature check itself is in `web-app-security-audit`, E3).
- **V7 Retries from the caller.** The endpoint is idempotent for methods that can be retried (see `data-consistency-review`, C1).
- **V8 Limits.** Pagination, maximum page size, payload size and rate limits are part of the contract and are returned to the caller when hit (HTTP 429 with a retry hint, or the equivalent status).
- **V9 Errors.** Error codes are stable and documented. The message can change; the code cannot.
- **V10 Contract tests.** The published schema or proto is checked against the implementation in the test suite, and a consumer test exists for each breaking-risk field. `NOT VERIFIED` if the suite cannot run in this review.
- **V11 Documentation.** The contract change is written where consumers read it, with an example request and response.

## Example

Input (illustrative): the diff renames `customer_name` to `name` in the response of `GET /customers/{id}`.

| ID | Check | Status | Severity | Evidence | Fix |
|---|---|---|---|---|---|
| V1 | Compatibility | FAIL | CRITICAL | `CustomerResponse.cs:12` (field renamed) | keep `customer_name` alongside `name`; deprecate it with a date |
| V3 | Deprecation | FAIL | HIGH | no deprecation note in the contract | mark `customer_name` deprecated and name its replacement |

## Related skills

Security of the same endpoints: `web-app-security-audit`. Rollout of the change: `release-safety-review`.

## Output

One table, the same format as `web-app-security-audit`: ID, check, status (`PASS`, `FAIL`, `N/A`, `NOT VERIFIED`), severity, evidence (`file:line`), fix. Then the fixes for every `FAIL` with `CRITICAL` or `HIGH` severity. Anything that needs a running system (load test, restore drill, production traffic) is `NOT VERIFIED` unless evidence is attached.

