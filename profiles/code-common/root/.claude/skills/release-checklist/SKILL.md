---
name: release-checklist
description: Verifies pre-release and deployment readiness, ensuring CI test passes, clean migrations, version bumps, security scans, and changelog updates.
---
# Pre-Release Checklist
1. **Tests & Build**:
   - Clean compilation without warnings or deprecation errors.
   - 100% test pass rate across unit, integration, and regression suites.
2. **Migrations & Database**:
   - Backward-compatible schema migrations verified.
   - Rollback scripts or rollback procedures tested.
3. **Security & Secrets**:
   - Automated secret scanners pass with zero leaks.
   - No vulnerable dependencies (lockfile audit green).
4. **Configuration & Environment**:
   - New environment variables documented with sensible defaults.
5. **Documentation & Changelog**:
   - Release notes updated with new features, fixes, and breaking changes.
   - Semantic versioning bumped appropriately.

# Output Format
`# | Item | Status (PASS / BLOCKED) | Verification Command / Evidence`

# Additional guidance
- Tests green: backend `Skipped: 0`; frontend `test` + `analyze` with no new warnings vs baseline; Rust `fmt`/`clippy -D warnings`/`test`.
- Review (`@reviewer`) and, if triggered, `@secops-engineer`. Migration: `check-migrations.py`, `dbcontext optimize`, tested with rows, **reversible** or a 2-phase plan.
- API contract changed → backend published first; the API doc updated. Rollback documented in `the runbook` (how to roll back app and database). Docs: the doc-check scripts compared with baseline. Builds for other platforms are **paused**: only with user confirmation.
- Deploy is done only by the user/authorized person: staging → smoke → production (canary if any) → observe 15 min (errors, p95, CAP/outbox queues). Rollback triggers (error rate > X%, p95 > X ms, critical flow fails, queue growing) are defined **before**; X from a measured baseline, else "not measured".
- Post: nominal metrics · changelog · close backlog items (`Status: ✅ Concluído` in the item's file). The agent does **not** deploy or notify anyone.
