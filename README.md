# Gatehouse

A team of AI agents you can drop into a repository, and the gates they pass work through. Each agent has a defined role, a voice and its own limits, and they hand work to each other through one structured handoff instead of a shared chat.

`AGENTS.md` is the canonical file. `.claude/` (Claude Code) links to the same agents and skills, and `.cursor/` (Cursor) links to the same rules, so one setup serves both.

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
| `template/` | What goes in your project root: `AGENTS.md`, `CLAUDE.md`, `.agents/` (9 agents, 47 skills, rules, a skills-by-signal index), symlinks for `.claude/` and `.cursor/`, settings, a session handoff file |
| `template/scripts/` | Deterministic checks the agents and CI can run: backlog tools, docs freshness gate, web and skill security scanners, scope check, Flutter analyze report (see below) |
| `template/docs/adr-examples/` | Four generic decision records (definition of done, leaf package, code in English, tests in every change) |
| `docs/` | Notes from evaluating popular skills |
| `profiles/` | Ready-made sets for a kind of repo (`code-repo`, `dart-package`, `flutter-app`); see [`profiles/README.md`](profiles/README.md) |
| `install.sh` | Copies `template/` or a profile into a repository without overwriting; `--check` lists drift |
| `tests/validate.sh` | Checks agent and skill frontmatter and that `install.sh` is idempotent |

The skills cover:

- **Specs and design:** `bdd-spec-writer`, `openspec-validation`, `adr-writer`, `tool-contract-design`, `threat-modeling`.
- **Review:** `owasp-sanitizer`, `web-app-security-audit` (fixed PASS / FAIL / N/A / NOT VERIFIED table), `data-consistency-review` (idempotency, locking, sagas, cache keys), `api-change-review` (compatibility, versioning, webhooks), `release-safety-review` (migrations, flags, rollback, backups), `infra-config-review` (Dockerfile, Kubernetes, Terraform, CI).
- **Testing:** `test-strategy`, `test-mutation-audit`, `authorized-testing` (scope, dummy fixtures, verification before a finding is reported).
- **Operations and quality:** `resilience-patterns`, `telemetry-tracing`, `performance-profiling`, `query-performance-tuner`, `incident-postmortem`, `release-checklist`, `root-cause-debug`, `tech-debt-triage`, `code-smell-eliminator`.
- **Backlog:** `backlog-items`, `backlog-triage`, `backlog-check`.
- **Writing:** `humanizer`, `token-optimization`, `ux-copy-ptbr`.

`template/.agents/SKILLS-INDEX.md` maps a task's signal (an API change, a login path, a Dockerfile) to the skills to load, so an agent reads one to three skills per pass instead of all of them.

## Scripts

All of them use the Python standard library only, and each has tests under `scripts/`.

| Script | What it does |
|---|---|
| `scripts/security/scan_web_patterns.py` | Mechanical pass of the web audit: public secrets, unsafe HTML, login without rate limit, client IP read from headers, hashing without a concurrency cap, cookies without `HttpOnly`. Every hit is a lead to read, not a verdict |
| `scripts/security/scan_skill_injection.py` | Finds instruction patterns that try to override authority, send data out, read credentials or chain shell commands, in agent and skill files. Defensive lines are excluded |
| `scripts/security/scope_check.py` | Checks a scope file (owner, authorizer, environment, dates, hosts) before any active test. Production is refused unless flagged |
| `scripts/backlog/check_backlog.py` | Integrity of a file-per-item backlog and its index |
| `scripts/backlog/triage_backlog.py` | One row per item, with facts only (open boxes, contradictions, empty bodies) |
| `scripts/backlog/new_item.py`, `set_status.py` | Create an item, or change its status in the file and the index together |
| `scripts/backlog/report_done.py` | Generates the done view from the item files |
| `scripts/backlog/split_backlog.py` | One-time migration of a single-file backlog; dry run by default |
| `scripts/backlog/check_doc_paths.py` | Links and backticked paths in Markdown that point to nothing |
| `scripts/docs/check_docs_fresh.py` | Freshness gate for generated docs, with pluggable generators (`generators/dependencies.py` draws the local dependency graph) |
| `scripts/lint/flutter_analyze_report.py` | Runs `flutter analyze` on every package and groups the issues by rule (read-only) |

## Agents

The `architect` applies `threat-modeling` to new trust boundaries and the three release-facing review skills to its design. The `reviewer` runs the web scanner and `web-app-security-audit` on changed routes. The `secops-engineer` applies `authorized-testing` before any test that sends traffic to a running system, and `threat-modeling` and `infra-config-review` to designs and build files.

## Use it

```bash
git clone https://github.com/samuelalvesg/gatehouse
./gatehouse/install.sh /path/to/your/project           # never overwrites
./gatehouse/install.sh /path/to/your/project --force   # overwrites
./gatehouse/install.sh /path/to/your/project --profile flutter-app   # a ready-made set instead of the template
```

Then:

1. Fill in the `<placeholders>` in `AGENTS.md` and `CLAUDE.md`: project, repository map, commit attribution, language.
2. Copy `.agents/agents/developer.md` once per stack (`backend-dev.md`, `frontend-dev.md`) and fill in "Stack".
3. Adapt the skills that name a stack (`owasp-sanitizer`, `test-strategy`, `a11y-audit`, `graph-mapping` use .NET, Flutter and Rust examples).
4. Install a profile instead of the template when the repo fits one (see `profiles/README.md`). Profiles copy the agents and skills of a kind of repo.

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
`frontend-dev` (in the template they are copies of `developer`), local-model (Ollama) profiles, the skill
`local-llama-bridge`, and the project's own MCP setup.

Not included: a full multi-agent security audit pack (Cloudflare's `security-audit`, about 315 KB, MIT). It is heavy and expects sub-agents and an isolated sandbox. Its guidance mode may be used on its own; see the backlog for the decision.
