---
name: threat-modeling
description: Structured threat model (data-flow diagram, trust boundaries, STRIDE per element, mitigations mapped to existing controls) for a new feature or a changed architecture. Use when a design introduces a new entry point, a new trust boundary, third-party data, or a new privileged role.
---

# Threat modeling

Model the design before the code is written, and again when it changes. The output is a list of threats each tied to a mitigation and an owner, not a generic list of risks.

## Procedure

1. **Diagram the data flow.** List external actors, processes, data stores and data flows. Mark every trust boundary (internet to server, service to database, tenant to tenant, app to third party).
2. **List the assets.** What must not leak, be changed, or stop working: credentials, personal data, money, quotas, availability of a core flow.
3. **Apply STRIDE per element.** For each process, data store, and flow that crosses a boundary, ask the six questions: Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege.
4. **Map each threat to a control.** Name the control that exists in the design, or mark the threat as open with an owner and a decision date.
5. **Check the controls you already have.** Point to the skill that verifies each one: `web-app-security-audit` (access, uploads, headers), `api-change-review` (contracts, webhooks), `data-consistency-review` (concurrency, cache, money), `infra-config-review` (containers, pipelines, IaC).

## Example

Input (illustrative): a new webhook endpoint `/hooks/payments` receives calls from a third party.

| Threat ID | Element | STRIDE | Threat | Control | Status | Owner |
|---|---|---|---|---|---|---|
| T1 | `/hooks/payments` | Spoofing | a fake sender calls the endpoint | HMAC signature check (`api-change-review` V6) | OPEN until the check is verified | backend dev |
| T2 | `/hooks/payments` | Denial of service | a flood of calls exhausts the worker | rate limit per source (`web-app-security-audit` G2) | OPEN | backend dev |

## Output

| Threat ID | Element | STRIDE | Threat | Control | Status | Owner |
|---|---|---|---|---|---|---|

Status: `MITIGATED` (control exists and is verified), `OPEN` (no control yet, decision needed), `ACCEPTED` (risk taken by a named person, with a reason). Never leave a threat without a status. A control that is described but not verified is `OPEN` until verified.

## Rules

- Do not invent threats to fill the table. A small, accurate model is better than a long one.
- Describe the design as it is, not as it should be. If the design is unknown, say so and mark the affected rows `NOT VERIFIED`.
- Re-run the model when a new trust boundary or a new privileged role appears.

## Related skills
- `api-change-review`: contract and webhook controls.
- `data-consistency-review`: concurrency, cache and money controls.
- `infra-config-review`: container, pipeline and IaC controls.
- `security-audit`: deeper audit modes.
- `web-app-security-audit`: checklist that verifies each control.
