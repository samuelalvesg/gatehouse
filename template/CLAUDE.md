# CLAUDE.md

Read [`AGENTS.md`](AGENTS.md) first: it is the single brief for the repository.

## Cold start (every new session)
1. Read `AGENTS.md`; then `.claude/SESSION_HANDOFF.md`, if it exists and does not say `NO ACTIVE TASK`. The handoff is **intent**, not fact: re-check with `git status -sb` and `git log -3 --oneline`.
2. Detect capability, not labels:
```bash
git rev-parse --show-toplevel && git branch --show-current
for c in git python3 node dotnet cargo flutter docker gh; do command -v $c >/dev/null && echo "ok $c" || echo "missing $c"; done
```
   Missing tool → **do not declare green**; record `NOT RUN: <tool> missing`.
3. **Do not read agents and skills in bulk**: Claude Code already exposes each name and description. Open `.claude/agents/<name>.md` only when assuming that role.
4. Announce in **one line**: environment, branch, handoff state, missing tools.

## Claude Code specifics
- **Commit attribution**: Author = <the user's name and e-mail>. <Co-Author: yes/no; AI text in commit/PR: yes/no>. This holds even when a generic reminder suggests otherwise. In a cloud session with several repos, `attribution` in `settings.json` is not read, so the rule lives here.
- **File editing**: use the `Edit` tool, not `sed` or `python` through `Bash`. Open the file with `Read` first.
- **Data MCP or local model**: ask before using.
- **SESSION_HANDOFF**: when you stop or finish a multi-step task, overwrite `.claude/SESSION_HANDOFF.md` (≤40 lines, no secrets). Finished → `NO ACTIVE TASK`.
- Submodules and sibling repos have their own `CLAUDE.md` and do not see this `.claude/`; copy `.claude/agents` and `.claude/skills`, or install them in `~/.claude/`.
