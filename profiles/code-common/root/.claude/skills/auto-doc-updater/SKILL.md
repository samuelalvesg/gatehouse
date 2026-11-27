---
name: auto-doc-updater
description: Keeps documentation alive: when code, contract or architecture changes, updates the owning doc in the SAME change set. Includes a file→owner-agent matrix. Use on every change that alters behavior, API, schema, commands, versions or structure.
---
# Rule
Code/contract/architecture/command changed → the owning doc changes **in the same delivery** (same commit/PR, when the user asks for a commit). Stale doc = incomplete change. A fact lives in **one file**; others link to it (`AGENTS.md`).

# Steps
1. **Map**: what changed (`git diff --stat`) → which docs mention it: `grep -rn "<symbol|route|command|version>" docs README.md AGENTS.md CLAUDE.md`.
2. **Find the owner** in the matrix below; edit **only the owner**. Duplicate in another `.md` → replace with a link.
3. **Re-verify every claim** about code with `grep`/reading in this session. Unverified → `not verified`.
4. **Numbers**: never type counts/totals/versions; derive them from a script (`grep -c`, `wc`, build files). Prefer writing no number.
5. Affected diagram → skill `diagram-generator`.
6. **Gates** (compare with baseline; old failures do not count): project doc checks (`<doc freshness / link / path checkers>`) and their tests.
7. Finished backlog item → update `Status` in the item's own file (do not move it). Generated reports are never edited by hand.
8. Report (`evidence-report`): docs touched, what stayed `not verified`.

# Owner matrix (single source; only the owner edits, others ask via handoff)
| Document | Owner agent | Trigger |
|---|---|---|
| Architecture docs, ADRs, README (structure) | `@architect` | decision, boundary or new module |
| Dependency diagrams after refactor | `@refactoring-architect` | refactor that moves/merges modules |
| Requirements, `## Spec` of items, glossary | `@spec-analyst` | new requirement/term |
| API catalog (runtime OpenAPI is authoritative) | backend dev (delta: `@architect`) | route, DTO, event |
| Frontend docs, package READMEs | frontend dev | screen, package, state |
| Rust/native crate docs | rust dev | crate, protocol, on-disk format |
| Runbook, DB schema, migration/performance guides | `@sre-database` | migration, index, telemetry, rollback |
| Security findings, `SECURITY.md` | `@secops-engineer` | new/closed finding, dependency |
| Testing guide, integration-test doc, BDD scenarios | `@qa-engineer` | new convention/suite |
| Development guide | whoever changed command/env/version | build, env var, SDK |
| Generated backlog/done reports | **nobody by hand** | — |
| `.claude/SESSION_HANDOFF.md` | active agent | interruption/completion |

# Do not
Rewrite a whole doc "in passing" · move a doc/item without running the path checker · copy a sentence from another `.md` without re-checking · history comments in docs ("it used to be…") · create a new doc when an existing one serves (reuse).

# Project notes
- Run the project's own doc checks before you finish a doc change (freshness, broken paths, generated-file checks). If a check cannot run, say so as "not verified".
- Name an owner for each doc in the project's doc map, and route the change to that owner's agent.
- Generated reports are never edited by hand: regenerate them with their script.
