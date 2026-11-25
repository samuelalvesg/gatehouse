# AGENTS.md - Brief for AI agents

The single canonical file for any agent (Claude Code, Cursor, Aider…).
`CLAUDE.md` points here. Detailed facts live in the linked files, not here.

## What the project is
<one sentence: what it is, stack, who uses it>

## Repository map
| Folder | Content |
|---|---|
| `<folder>` | <...> |

## Where to read before changing something
| Task | Read first |
|---|---|
| <task> | <link> |

## Critical conventions
- **Tests in every implementation**: every code PR has unit and integration tests for the change; a bug fix has a regression test. Reuse the existing helpers.
- **Language**: code, comments and test names are in English. Documents you create or touch are in English; a legacy document that you do not touch stays in its language until you edit it, then it is converted to English. Commit messages follow <project language>. Text shown to the user follows <project language>. Do not translate an existing file "in passing".
- **Comments**: only the non-obvious **why**. Never history ("it used to be X") and never what the name already says; that belongs in `git blame` and in the commit.
- **Reuse instead of duplicating.** A finding or debt goes to the **backlog**, not to the chat.
- **Documentation**: a claim about the code's state only with `grep` or reading in this session; otherwise "not verified". Numbers in documents come from a script.
- **Number of PRs**: as few as possible. Gather related changes into one PR, as a **draft**; mark it ready only at the end. CI runs only when a PR is marked ready for review. The user does the merge.
- **Git**: commit and push only when the user asks; never directly on the main branch; never `--force` or `reset --hard` on someone else's branch.

## Agent team (`.agents/agents/`, `.agents/skills/`)
Pipeline: `@spec-analyst` → `@architect` → `@developer` (one copy per stack) → `@qa-engineer` → `@reviewer`.
By trigger: `@secops-engineer` (security, dependencies, release), `@sre-database` (migration, query, telemetry), `@refactoring-architect` (debt, separate diff), `@copywriter-humanizer` (writing and humanized review of documents, PRs, issues and UI text).

- **One owner at a time.** Only `@architect` and `@spec-analyst` change spec and contract; only developers change production code; only `@qa-engineer` changes acceptance tests; `@reviewer` and `@secops-engineer` only read.
- **Handoff** is the only channel between agents (≤25 lines). Protocol keywords and fields are in English, because agents parse them:
```
HANDOFF @de → @para
ITEM: <caminho do item de backlog>
SCOPE: <arquivos/módulos que PODEM mudar>
OUT: <o que NÃO mexer>
CONTRACT: <rota/DTO/evento, antes → depois>
SCENARIOS: <ids da spec que o QA vai testar>
RISKS: <migration? contrato? multi-tenant?>
ORDER: <quem primeiro>
ENVIRONMENT: <shell? ferramentas que faltam>
```
- **Return** (keywords in English, as agents parse them): `RETURN @de → @para | STATUS: OK|BLOCKED|DIVERGENT` + DONE / NOT RUN / PENDING. Outside SCOPE or a divergent spec → `BLOCKED` to `@architect`; never expand the scope alone.
- In Claude Code: the `Agent` tool with `subagent_type: <name>` and the literal handoff as the prompt (the subagent does not inherit the conversation). Without subagents: open `.claude/agents/<name>.md` and switch role by writing `[ROLE: @name]`.

**Hard limits (no agent does these alone):** merge or a PR marked ready without green tests; touching credentials, `.env` or production; deleting what it did not create; sending data to an external service; weakening, skipping or deleting a test to make it pass.

## Useful commands
<build / test / lint>
