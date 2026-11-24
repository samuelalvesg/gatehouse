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

## Agents and skills

### Agents (9)

| Agent | Role |
|---|---|
| `architect` | Solution architect and specification guardian. |
| `copywriter-humanizer` | Expert in humanizing text and copywriting for humans. |
| `developer` | Software engineer template. |
| `qa-engineer` | Quality assurance engineer. |
| `refactoring-architect` | Refactoring specialist. |
| `reviewer` | Strict code review (correctness, security, repository standards). |
| `secops-engineer` | Security operations engineer. |
| `spec-analyst` | Requirements analyst. |
| `sre-database` | Reliability and database specialist. |

### Skills (47)

| Skill | What it covers |
|---|---|
| `a11y-audit` | Accessibility audit (WCAG 2.1/2.2 AA) for Flutter/Web screens. |
| `adr-writer` | Writes Architecture Decision Records (Nygard format) and diagrams systems with explicit requirements, alternatives, and trade-offs. |
| `api-change-review` | Review of a change to a public or cross-team API (HTTP, gRPC, events, webhooks): compatibility, versioning, deprecation, delivery guarantees and limit |
| `authorized-testing` | Rules for any active test of a system (validating a finding, probing a staging app, checking a control under load): written scope, authorization, safe |
| `auto-doc-updater` | Keeps documentation alive: when code, contract or architecture changes, updates the owning doc in the SAME change set. |
| `backlog-check` | Run the backlog integrity checks (index and item agreement, orphans, done rules) as a gate before finishing a change that touches backlog files. |
| `backlog-items` | Model and rules for a file-per-item backlog (one file per item, a Status field, an index table). |
| `backlog-triage` | Read a file-per-item backlog and report facts about it (open and done items, contradictions, empty bodies) without editing anything. |
| `bdd-spec-writer` | Writes executable BDD scenarios (Given/When/Then) with clear acceptance criteria and edge cases. |
| `code-smell-eliminator` | Identifies and eliminates code smells, dead code, excessive complexity, and architectural degradation without altering behavior. |
| `data-consistency-review` | Review of how a change keeps data correct under concurrency, retries and partial failure (idempotency, locking, check-then-act, sagas, outbox, dead-le |
| `diagram-generator` | Generates and updates Mermaid diagrams (flow, sequence, ER, C4, dependency) inside .md files, from real code and with per-part status. |
| `docling` | > |
| `dotnet-flutter-hotspots` | Review checklist of frequent defects in C#/.NET services and Flutter/Dart apps: async misuse, EF Core pitfalls, DI lifetimes, cancellation, disposal,  |
| `evidence-report` | Generates fact-based evidence reports for code reviews, QA audits, and security assessments. |
| `fault-injection-testing` | Test strategies beyond the happy path: fault injection, property-based tests, fuzzing, deterministic time/clock, contract tests, replay/soak/chaos for |
| `find-skills` | Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or e |
| `flutter-design-system` | Enforces Flutter Design System and OpenDesign standards, ThemeData/ColorScheme token inheritance, responsive widget architecture, micro-interactions,  |
| `graph-mapping` | Maps dependencies and blast radius (callers, dependents) before modifying code. |
| `grill-me` | A relentless interview to sharpen a plan or design. |
| `humanizer` | | |
| `improve-codebase-architecture` | Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick. |
| `incident-postmortem` | Generates blameless post-mortem analysis from incidents, regressions, or production bugs. |
| `infra-config-review` | Review of infrastructure and delivery configuration (Dockerfiles, Compose, Kubernetes manifests, Terraform, CI pipelines, environment files) for privi |
| `iot-automation-design` | Guides design and review of IoT/industrial automation data paths (Modbus, OPC UA, MQTT, gRPC, edge gateways, SCADA-like dashboards, rules/automation): |
| `openspec-validation` | Validates functional and technical specifications against OpenSpec standards, ensuring completeness, testability, contract consistency, and unambiguou |
| `owasp-sanitizer` | Audits code and dependencies against OWASP Top 10 vulnerabilities, insecure defaults, sanitization flaws, authentication bypasses, and secret leaks. |
| `performance-profiling` | Measures and improves performance across C#, Rust and Flutter: define a budget, profile before changing, optimize the hot path, prove the gain with a  |
| `query-performance-tuner` | Analyzes execution plans (EXPLAIN ANALYZE), indexing and N+1 in Postgres/EF Core. |
| `release-checklist` | Verifies pre-release and deployment readiness, ensuring CI test passes, clean migrations, version bumps, security scans, and changelog updates. |
| `release-safety-review` | Review of how a change is rolled out and reversed (schema migrations, feature flags, blue-green, canary and rolling deploys, rollback, health checks,  |
| `resilience-patterns` | Designs and reviews resilience for services, workers, edge gateways and offline-first apps: timeouts, retries with jitter, circuit breakers, bulkheads |
| `root-cause-debug` | Investigates software bugs and unexpected behaviors down to their fundamental root cause using structured hypotheses and reproducible evidence, not su |
| `rust-async-safety` | Review checklist for Rust services, edge collectors and FFI crates: error handling, async/tokio pitfalls, concurrency, unsafe/FFI boundaries, memory a |
| `tech-debt-triage` | Analyzes, categorizes, and prioritizes technical debt, legacy code, and architectural inconsistencies into actionable backlog tasks with clear risk/re |
| `telemetry-tracing` | Structured logs, health metrics and distributed tracing (OpenTelemetry) without degrading performance or leaking data. |
| `test-mutation-audit` | Evaluates test suite quality and coverage by introducing artificial faults (mutations) to verify that tests fail when code is defective. |
| `test-strategy` | Defines test coverage plans, test level distribution (unit, integration, contract, E2E), edge cases, and regression test suites for new features and b |
| `threat-modeling` | Structured threat model (data-flow diagram, trust boundaries, STRIDE per element, mitigations mapped to existing controls) for a new feature or a chan |
| `to-tickets` | Break a plan, spec, or the current conversation into a set of tracer-bullet tickets, each declaring its blocking edges, published to the configured tr |
| `token-optimization` | Enforces high-density conciseness, prompt token optimization, and zero conversational filler across all agent interactions. |
| `tool-contract-design` | Designs reliable, safe, and robust tool contracts (MCP / CLI tools) with explicit input schemas, strict validation, and structured error responses. |
| `ui-handoff-spec` | Generates UI/UX handoff specifications for frontend developers, mapping components, interaction states, responsive layouts, design tokens, and error h |
| `ui-ux-pillars` | UI/UX review checklist for Flutter shared components and screens, grounded in Material 3 adaptive guidance, WCAG 2.2 and NN/g heuristics. |
| `ux-copy-ptbr` | Brazilian Portuguese (pt-BR) interface copy guidelines (buttons, errors, empty states, confirmation dialogs). |
| `verify-delivery` | Runs this repository's delivery gate (build, lint, tests, migration checks) and reports PASS, FAIL or NÃO EXECUTADO per command. |
| `web-app-security-audit` | Pre-launch security audit of a web app (API routes, auth, uploads, webhooks, client bundles, database policies) as a fixed PASS/FAIL/N/A/NOT VERIFIED  |

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
| `scripts/tests/repeat_test.py` | Runs a test command N times and reports the pass rate: always failing vs flaky |
| `scripts/tests/check_skipped.py` | Fails when a test run skipped more tests than allowed (dotnet, pytest, jest) |
| `scripts/lint/detect_duplicates.py` | Finds blocks of code repeated across files, to reuse instead of copy |
| `scripts/i18n/check_l10n_completeness.py` | Checks each translation file has the reference language's keys |
| `scripts/monitor/monitor_android.sh` | Samples RAM and CPU of one Android app over adb, as CSV |
| `scripts/lint/flutter_analyze_report.py` | Runs `flutter analyze` on every package and groups the issues by rule (read-only) |

## How the agents use the skills

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
