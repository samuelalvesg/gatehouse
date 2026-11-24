---
name: token-optimization
description: Enforces high-density conciseness, prompt token optimization, and zero conversational filler across all agent interactions. Use to cut context bloat and token consumption without loss of technical accuracy.
---
# Rules for Maximum Conciseness ("Be Concise")
1. **Zero Conversational Filler**:
   - Eliminate all polite pleasantries ("Sure!", "I would be happy to help with that", "Certainly").
   - Eliminate staged run-ups ("Here is the solution:", "Let's dive into...").
   - Start immediately with the answer, action, diagnosis, or code diff.
2. **Direct Fact-First Structure**:
   - Format: `[Context/Issue] -> [Root Cause / Key Action] -> [Implementation / Fix]`.
   - Use direct statements and fragments where syntax clarity allows.
3. **Targeted Reading & Diffing**:
   - Read specific line ranges instead of dumping entire source files.
   - Output minimal unified diffs and surgical edits; avoid reprinting large untouched blocks.
4. **Structured Handoffs**:
   - Handoffs between agents strictly <= 25 lines.
5. **Code Integrity**:
   - Code blocks, variable names, and error traces remain 100% technically exact and intact.

# Additional guidance
- Read the minimum (`grep`/`Read` with `offset`/`limit` before whole files; diff before file; do not re-read what you just edited); parallelize independent reads; one fact, one place (link the owning `.md`).
- Optimization order when designing an agent/tool: 1) tokens and context (smallest sufficient answer, with provenance; count schemas, extra calls and retries), 2) time, 3) CPU/memory. "Fewer bytes" does not prove "fewer tokens": measure the full task and label estimates.
- Never compress: code, commands, paths, literal error messages; security warnings, destructive actions, confirmation requests; `.md` docs, commit messages and UI text; evidence (numbers, test output, `file:line`).
- Budgets: handoff 25 lines · dev/QA report 15 · review 40 · graph-mapping output 30. Final check: cut the first and last sentence of each answer; if nothing was lost, leave them cut.
