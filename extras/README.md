# Extras

Material that is **not** installed by `install.sh` and that agents must not load by default.

| Folder | What it is | When an agent may read it |
|---|---|---|
| `security-audit/` | Cloudflare's multi-agent security audit skill (MIT). Heavy: sub-agents, an isolated sandbox, artifacts written outside the repository. | Only when the user explicitly asks for a complete audit or pen test of a codebase. Otherwise use `template/.agents/skills/web-app-security-audit` and the scanners. |

Rules:

1. Nothing here is referenced from `template/`, `profiles/` or a skill's default path.
2. An agent reads a file in this folder only after the user asks for the matching case above, and says which file it is reading.
3. Running the validators in `security-audit/` needs the user's approval, because it executes third-party code.
