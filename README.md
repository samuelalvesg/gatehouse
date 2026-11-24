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
| `projects/` | Text to paste into Claude Projects (instructions and starting memory) |
| `environments/` | A setup script for a cloud environment, as a model |
| `docs/` | Inventory of the original setup and the gaps found |
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
4. Paste `projects/INSTRUCOES_CLAUDE_PROJECTS.md` and `projects/MEMORIA_INICIAL.md` into your project on claude.ai.

## Good to know

- `AGENTS.md`, `CLAUDE.md`, the `projects/` texts and parts of `docs/` are in Brazilian Portuguese; the agent files are in English. Translate what you need.
- Left out on purpose because they are tied to the original project: stack-specific developers, local-model (Ollama) profiles and a few skills such as `local-llama-bridge` and `telemetry-tracing`.
- Several skills derive from Apache-2.0 plugins; see `template/.claude/NOTICE.md`.
## Plugins declarados no repo

Plugin instalado só na conta do claude.ai vale para quem tem a conta. Para que
qualquer sessão que abra o repo receba o plugin, declare em
`.claude/settings.json` (o template já traz `code-review`):

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

Escolha por stack: .NET → `csharp-lsp` (precisa de `csharp-ls`); Rust →
`rust-analyzer-lsp` (precisa de `rust-analyzer`); Flutter → `dart-flutter`.
O setup de `environments/` instala os dois servidores. Plugin sem
`marketplace.json` público (por exemplo `backend-design`) não dá para declarar:
fica na conta, e os agentes o citam como "usar se carregado". Copiar skill de
plugin para o repo só quando for adaptar, com a origem no `NOTICE.md`.
`tests/validate.sh` reprova plugin cujo marketplace não está declarado.

A skill `verify-delivery` é o gate de entrega do repo: preencher os comandos
(os mesmos do CI). `@developer`, `@qa-engineer` e `@reviewer` a citam.

## Perfis dos repositórios example

`profiles/` guarda a configuração exata dos repos example, example-backend,
example-frontend e example-edge (agentes com SOUL, skills, regras, MCP, plugins):
este repo é a fonte e os repos recebem a cópia com
`./install.sh <repo> --profile <nome> --force`; `--check` confere se a cópia do
repo continua igual. Detalhes em [`profiles/README.md`](profiles/README.md).

## Fora do template (de propósito)

`rust-dev` e `backend-dev`/`frontend-dev` específicos (viram cópias do `developer`), perfis de modelo local (Ollama), skills `local-llama-bridge`, `auto-doc-updater`, `diagram-generator`, `query-performance-tuner`, `telemetry-tracing`, `ux-copy-ptbr` e o `.agents/` (MCP próprios): acopladas ao example. Estão em `profiles/`, não em `template/`.

## License

Apache-2.0
