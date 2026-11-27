---
name: adr-writer
description: Writes Architecture Decision Records (Nygard format) and diagrams systems with explicit requirements, alternatives, and trade-offs. Use for decisions on architecture, tech stack, or module boundaries.
---
# Repository Convention
Use the project's ADR folder (commonly `docs/adr/` or `docs/ADR/`). File `NNNN-short-title.md` (next sequential number; check the folder). Sections: **Status** (`Accepted|Proposed|Deprecated|Under review`), **Context**, **Decision**, **Consequences**. Accepted ADRs are immutable: write a new ADR and mark the previous one `Deprecated`. Update the index in the folder's README.

# Before Writing
Search the ADR folder and the project backlog for prior decisions (do not relitigate accepted decisions). Identify functional/non-functional requirements (scale, latency, cost, team), constraints.

# Decision Structure
1. Requirements and constraints (numbered).
2. >= 2 alternatives, including "do nothing": complexity, cost, scale, team familiarity, reversibility.
3. Trade-off summary in 3-5 lines; single recommendation.
4. Consequences: what becomes easier, harder, and what to revisit (measurable trigger).
5. Mermaid diagram showing packages and state.

# Rules
Verify codebase facts using active grep/read operations; otherwise state "not verified". Price, license, and legal aspects must be escalated to the user.

# Output
Ready-to-commit ADR file and index line update. Status `Proposed` until confirmed by user.

# Options considered
- At least two real options, each with the trade-off it gives up, and why it was rejected.

# Consequences
- What becomes easier, what becomes harder, and the follow-up actions with owners.

# Diagrams
- Show packages and what is decided. Mark each part's state: ✅ exists, 🟡 partial, 📝 only recorded, ❓ open. Check the state in the code, or mark it "not verified".
