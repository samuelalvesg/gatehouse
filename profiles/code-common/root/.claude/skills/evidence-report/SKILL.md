---
name: evidence-report
description: Generates fact-based evidence reports for code reviews, QA audits, and security assessments. Every claim must link directly to concrete lines of code or test executions.
---
# Evidence Reporting Standards
- Zero unverified assumptions: Every finding must include `file:line`, the observed behavior, and the expected behavior.
- Reproducible steps: Include the exact command or test invocation used to verify the condition.
- Severity classification:
  - **BLOCKER**: Prevents merge/release; data corruption, security vulnerability, contract violation.
  - **CORRECT**: Functional defect, missing test, unhandled edge case.
  - **SUGGESTION**: Style refinement, non-blocking cleanup (maximum 3 suggestions).

# Report Template (<= 40 lines)
```markdown
# Evidence Report: <Task / PR Title>
- **Date**: YYYY-MM-DD
- **Scope**: <Files / Components verified>

## Findings
1. [<SEVERITY>] `<path/to/file>:<line>`
   - **Observed**: <Actual behavior / defect>
   - **Expected**: <Contract / Spec requirement>
   - **Remediation**: <Concrete fix>

## Verification
- Tests executed: `<command>` -> PASS / FAIL

## Verdict
APPROVED | APPROVED WITH NOTES | REJECTED
```

# Additional guidance
Evidence levels: OBSERVED / DERIVED / INFERRED / UNKNOWN. Finding classes: `REPRODUCED DEFECT` (steps + output; only this one counts as a bug) · `SUPPORTED LIMITATION` · `DESIGN OPPORTUNITY` · `HYPOTHESIS` · `EVIDENCE UNAVAILABLE`. Minimum fields: `FINDING | LEVEL | EVIDENCE (file:line or command+output) | COVERAGE | LIMITE/NOT VERIFIED | ACTION`. Missing data: write `INSUFFICIENT DATA: <what is missing>` and ask. Group duplicates by root cause. Never repeat a fact from another `.md` without re-checking (`AGENTS.md` documentation rule).
