---
name: verify-delivery
description: Runs this repository's delivery gate (build, lint, tests, migration checks) and reports PASS, FAIL or NÃO EXECUTADO per command. Use before handing off to @qa-engineer or @reviewer, before marking a PR ready, and whenever someone asks whether it is green.
---

# Verify delivery

## Rules
- Detect capability first: `command -v <tools of the stack>`. Missing tool →
  `NÃO EXECUTADO: <tool> ausente`; never report green.
- Never skip, weaken or delete a test to get green.
- While fixing, re-run only what failed; the full gate again at the end.
- A test runner that skips tests silently (database, container, device) is
  FAIL until the skip count is zero or each skip is explained.
- Keep only failures, totals and skip lines; drop green logs.

## Commands
<Comandos de entrega na ordem, os mesmos do CI>

Examples by stack (replace the placeholder above and delete this list):
- .NET: Docker up; `dotnet test <path>/Tests.csproj`; require `Skipped: 0`.
- Flutter/melos: `melos bootstrap`; `flutter analyze` and `flutter test` in the touched package.
- Rust: `cargo fmt --all --check`; `cargo clippy --workspace --all-targets --locked -- -D warnings`; `cargo test --workspace --locked`.
- Node: `npm ci`; `npm run lint`; `npm test`.

## Report (same block in the PR body and in `SESSION_HANDOFF.md`)
```
VERIFY: <repo> @ <short sha>
<command> → PASS | FAIL (<n>) | NÃO EXECUTADO: <motivo>
SUITE: total / passed / failed / skipped
```
