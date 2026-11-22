# claude-agents

Template reutilizável de equipe de agentes para Claude Code, extraído dos repositórios
example, example-backend, example-frontend e example-edge (ver [`docs/INVENTARIO.md`](docs/INVENTARIO.md)).

## O que tem

| Pasta | Conteúdo |
|---|---|
| `template/` | O que vai para a raiz do projeto novo: `AGENTS.md`, `CLAUDE.md`, `.agents/` (agents, skills, rules), links simbólicos em `.claude/` e `.cursor/`, settings, SESSION_HANDOFF, NOTICE. |
| `projects/` | Texto para colar no **Claude Projects** (instruções e memória) e a lista do que trabalhar. |
| `environments/` | Setup script do ambiente de nuvem (campo "Setup script"). `example-setup-env.sh`: .NET 10, Flutter, Docker, Rust; versões por variável de ambiente. Específico do example: usar como modelo. |
| `docs/` | Inventário das configurações existentes e lacunas encontradas. |
| `install.sh` | Copia `template/` para um repo, sem sobrescrever o que já existe. |

## Uso

```bash
./install.sh /caminho/do/projeto          # não sobrescreve
./install.sh /caminho/do/projeto --force  # sobrescreve
```

Depois:
1. Preencher os `<placeholders>` de `AGENTS.md` e `CLAUDE.md` (projeto, mapa, atribuição de commit, idioma).
2. Copiar `.agents/agents/developer.md` uma vez por stack (`backend-dev.md`, `frontend-dev.md`…) e preencher "Stack".
3. Adaptar as skills que citam stack (`owasp-sanitizer`, `test-strategy`, `a11y-audit`, `graph-mapping`: exemplos .NET/Flutter/Rust).
4. Colar `projects/INSTRUCOES_CLAUDE_PROJECTS.md` e `projects/MEMORIA_INICIAL.md` nas configurações do projeto no claude.ai.

## Equipe

`spec-analyst` → `architect` → `developer` → `qa-engineer` → `reviewer`; por gatilho `secops-engineer`, `sre-database`, `refactoring-architect`, `copywriter-humanizer`. Handoff estruturado é o único canal entre agentes.

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

## Fora do template (de propósito)

`rust-dev` e `backend-dev`/`frontend-dev` específicos (viram cópias do `developer`), perfis de modelo local (Ollama), skills `local-llama-bridge`, `auto-doc-updater`, `diagram-generator`, `query-performance-tuner`, `telemetry-tracing`, `ux-copy-ptbr` e o `.agents/` (MCP próprios): acopladas ao example. Copiar do repo de origem sob demanda.

Licença Apache-2.0; ver `template/.claude/NOTICE.md` para skills derivadas.

Teste: `tests/validate.sh` (frontmatter de agentes/skills e idempotência do `install.sh`).
