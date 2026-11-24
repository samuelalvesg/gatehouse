---
name: openspec-validation
description: Validates functional and technical specifications against OpenSpec standards, ensuring completeness, testability, contract consistency, and unambiguous acceptance criteria.
---
# Checklist
1. **Unambiguous Requirements**: No vague qualifiers ("fast", "scalable", "user-friendly") without measurable numeric targets (e.g. p95 < 200ms).
2. **Contract Completeness**: Endpoints, schemas, DTOs, headers, status codes, and error payloads explicitly defined.
3. **State Transitions**: Valid and invalid state transitions documented (idempotency, concurrency, race conditions).
4. **Failure Modes**: Explicit behavior defined for timeouts, network disconnects, third-party outages, and invalid authentication.
5. **Traceability**: Each requirement maps directly to at least one testable acceptance scenario (Given/When/Then).

# Validation Report Format
- **Specification**: `<document-path>`
- **Verdict**: `VALID | NEEDS REVISION | INCOMPLETE`
- **Missing Items**: List of gaps or ambiguities (severity: Critical, Major, Minor).
- **Recommended Fixes**: Concrete suggestions to resolve each gap.

# Additional guidance
- Home: `## Spec` section of the `docs/backlog/` item (reuse, no new folder). Lasting requirement → also the requirements doc; decision → ADR.
- Format: `### R1 <name>` + `The system SHALL …` + `#### Cenário R1.1` with WHEN/THEN, `### Delta de contrato` (ADDED/MODIFIED/REMOVED, with consumers via `graph-mapping`), `### Fora de escopo`.
- Domain terms must match `the glossary`; edge cases explicit (empty, null, wrong tenant, soft-deleted, permission denied, idempotency); contract break → backend first + plan for the app. Output: `SPEC OK` or a numbered list of what is missing (≤10 lines); scenario ids go in the handoff and become test names for `@qa-engineer`.
