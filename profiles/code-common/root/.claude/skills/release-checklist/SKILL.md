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

# Rollback triggers
- Conditions that start a rollback without debate: error rate or latency above the agreed threshold, a failed health check, data integrity errors, a security finding.
- The rollback path for each change: previous artifact, feature flag to turn off, and whether a migration needs a reverse step or only a forward fix.

# Post-deploy
- Watch the agreed signals for the first period after the release (errors, latency, the business metric that matters). Confirm the new version is the one serving traffic.
- Record the outcome and close the release item in the backlog, or open a follow-up for anything still open.

# Additional guidance
- Tests green with no skipped tests; static analysis with no new warnings vs baseline; formatter and linter clean.
- Review (`@reviewer`) and, if triggered, `@secops-engineer`. Migrations: run the project's migration check, test against a database with existing rows, and keep them **reversible** or use a two-phase plan.
- API contract changed → backend published first; the API doc is updated in the same release.
- Deploy is done only by the user/authorized person: staging → smoke → production (canary if any) → observe 15 min (errors, p95, message queues). Rollback triggers (error rate > X%, p95 > X ms, critical flow fails, queue growing) are defined **before**; X from a measured baseline, else "not measured".
- Post: nominal metrics · changelog · close backlog items (`Status: ✅ Concluído` in the item's file). The agent does **not** deploy or notify anyone.

# Project release gates
- If the API contract changed, ship the backend first and update the API document in the same release.
- Document rollback for the app and for the database in the runbook.
- Run the project's documentation checks and compare the result with the baseline.
- Build only the platforms the release owner has confirmed.
