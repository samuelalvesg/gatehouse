---
name: root-cause-debug
description: Investigates software bugs and unexpected behaviors down to their fundamental root cause using structured hypotheses and reproducible evidence, not superficial patches.
---
# Systematic Debugging Protocol
1. **Reproduce**: Establish a minimal, reproducible test case or script demonstrating the failure consistently.
2. **Isolate**: Formulate competing hypotheses. Test one variable at a time via binary search (git bisect, targeted unit test, isolated execution).
3. **Trace**: Inspect logs, stack traces, variable values, and timing. Differentiate symptoms from root causes.
4. **Identify Root Cause**: State exactly why the defect occurs (e.g. state mutation, unhandled race condition, precision loss, schema mismatch).
5. **Verify Fix**: Implement the minimal fix. Confirm that the reproducible test now passes and no existing tests regress.
6. **Regression Guard**: Commit the regression test alongside the fix.

# Diagnostic Output (<= 25 lines)
```
BUG: <description>
REPRODUCTION: <command or test case>
ROOT CAUSE: <file:line + technical explanation>
PROPOSED FIX: <minimal diff explanation>
REGRESSION TEST: <new test path>
```

# Additional guidance
- Stack shortcuts (examples): 500+ tests "passing" but skipped → Docker is down, check "Skipped". 400 at runtime with a clean build → EF compiled models: `dotnet ef dbcontext optimize`. Migration breaks with existing rows → primitive collection without `HasDefaultValueSql`. Mass 401 / photos → request fallback without crash.
- Isolate: `git log -p --since=... -- <path>`, `git bisect` if a known-good commit exists; logs by `TraceId` (`telemetry-tracing`).
- Fix order: regression test red first (`@qa-engineer`), then fix, then green. Once the cause is found, `grep` sibling consumers/adapters with the same pattern, **group by root cause**, and fix at the **producer** before patching consumers.
- Limits: no production/project data/model MCP unless asked; never "fix" a test to pass; assert a cause only with evidence. Output: `SYMPTOM | REPRODUCTION | ROOT-CAUSE (evidência) | FIX | TEST DE REGRESSÃO | PREVENÇÃO`.
