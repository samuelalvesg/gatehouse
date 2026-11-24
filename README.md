# claude-agents

A team of agents for Claude Code that you can drop into a repository. Each agent has a defined role and voice, and its own limits. They pass work to each other through one structured handoff instead of a shared chat.

It was extracted from a multi-repo project (Flutter, .NET and Rust) that uses it every day.

## The team

`spec-analyst` → `architect` → `developer` → `qa-engineer` → `reviewer`

Called by trigger, not on every change: `secops-engineer` (security and dependency risk), `sre-database` (migrations, queries, performance), `refactoring-architect` (debt, in a separate diff from features) and `copywriter-humanizer` (docs, PR text, UI copy).

Rules that apply to everyone:

- The handoff is the only channel between agents. Context outside it is lost on purpose.
- One owner at a time. Only the architect and the analyst change specs and contracts, only developers change production code, and the reviewer and secops only read.
- A change outside the handoff's scope goes back to the architect. Nobody widens it alone.
- Never weaken, skip or delete a test to make it pass.

## What is inside

| Folder | Content |
|---|---|
| `template/` | What goes in your project root: `AGENTS.md`, `CLAUDE.md`, `.agents/` (9 agents, 25 skills, rules), symlinks for `.claude/` and `.cursor/`, settings, a session handoff file |
| `docs/` | Notes from evaluating popular skills |
| `install.sh` | Copies `template/` into a repository without overwriting |
| `tests/validate.sh` | Checks agent and skill frontmatter and that `install.sh` is idempotent |

The skills cover specs (`bdd-spec-writer`, `openspec-validation`), design (`adr-writer`, `tool-contract-design`), quality (`test-strategy`, `test-mutation-audit`, `evidence-report`), security (`owasp-sanitizer`), debugging (`root-cause-debug`, `incident-postmortem`), debt (`code-smell-eliminator`, `tech-debt-triage`) and writing (`humanizer`, `token-optimization`).

## Use it

```bash
git clone https://github.com/samuelalvesg/claude-agents
./claude-agents/install.sh /path/to/your/project           # never overwrites
./claude-agents/install.sh /path/to/your/project --force   # overwrites
```

Then:

1. Fill in the `<placeholders>` in `AGENTS.md` and `CLAUDE.md`: project, repository map, commit attribution, language.
2. Copy `.agents/agents/developer.md` once per stack (`backend-dev.md`, `frontend-dev.md`) and fill in "Stack".
3. Adapt the skills that name a stack (`owasp-sanitizer`, `test-strategy`, `a11y-audit`, `graph-mapping` use .NET, Flutter and Rust examples).

## Good to know

- `AGENTS.md` and `CLAUDE.md` are in Brazilian Portuguese; the agent files are in English. Translate what you need.
- Several skills derive from Apache-2.0 plugins; see `template/.claude/NOTICE.md`.

## Plugins declared in the repo

A plugin installed only on a claude.ai account works only for people with that
account. To make every session that opens the repo get the plugin, declare it
in `.claude/settings.json` (the template already ships `code-review`):

```json
"extraKnownMarketplaces": {
  "claude-plugins-official": { "source": { "source": "github", "repo": "anthropics/claude-plugins-official" } },
  "dart-flutter": { "source": { "source": "github", "repo": "flutter/agent-plugins" } }
},
"enabledPlugins": {
  "code-review@claude-plugins-official": true,
  "csharp-lsp@claude-plugins-official": true,
  "rust-analyzer-lsp@claude-plugins-official": true,
  "dart-flutter@dart-flutter": true
}
```

Pick by stack: .NET → `csharp-lsp` (needs `csharp-ls`); Rust →
`rust-analyzer-lsp` (needs `rust-analyzer`); Flutter → `dart-flutter`.
A plugin with no public
`marketplace.json` (for example `backend-design`) can't be declared. It stays
on the account, and the agents mention it as "use if loaded". Copy a plugin's
skill into the repo only when you are going to adapt it, and record the origin
in `NOTICE.md`. `tests/validate.sh` fails any plugin whose marketplace isn't
declared.

The `verify-delivery` skill is the repo's delivery gate: fill in its commands
(the same ones as CI). `@developer`, `@qa-engineer` and `@reviewer` refer to it.

## Left out of the template on purpose

These are tied to the project the template came from: `rust-dev`, the stack-specific `backend-dev` and
`frontend-dev` (in the template they are copies of `developer`), local-model (Ollama) profiles, the skills
`local-llama-bridge`, `auto-doc-updater`, `diagram-generator`, `query-performance-tuner`, `telemetry-tracing`
and `ux-copy-ptbr`, and the project's own MCP setup.
