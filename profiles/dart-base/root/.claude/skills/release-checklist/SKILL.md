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
