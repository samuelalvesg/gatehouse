---
name: code-smell-eliminator
description: Identifies and eliminates code smells, dead code, excessive complexity, and architectural degradation without altering behavior. Use for technical debt reduction and refactoring tasks.
---
# Principles
- Behavior preservation: Existing tests MUST pass before and after refactoring. Never combine refactoring with behavioral changes.
- Small atomic steps: Rename, extract method, move class, inline variable one step at a time. Commit incrementally.
- Eliminate duplication: Apply DRY strictly across domain services, helpers, and DTOs.
- High cohesion, low coupling: Ensure classes have a single reason to change (SRP).

# Smell Catalog & Fixes
- Long Method: Extract method / delegate to private helper or domain service.
- Large Class: Extract sub-components, split into focused handlers/services.
- Primitive Obsession: Introduce Value Objects with validation.
- Long Parameter List: Introduce Parameter Object or options record.
- Feature Envy: Move behavior closer to the data owner.
- Dead Code: Verify zero references via grep/AST before deleting.

# Output
Summary of smells eliminated, before/after diff summary, and verification test status.

# Additional guidance
- Size limits: `.agents/rules/frontend-clean-code-rule.md` (Dart) and `.agents/rules/code-syle-rule.md` (C#). Cyclomatic complexity: `dotnet build` with rule CA1502, `dart analyze`/DCM; otherwise count `if/for/while/case/&&/||/catch`; practical target ≤10 per method.
- Missing coverage → ask `@qa-engineer` for a characterization test. Never translate a file to English in passing. Duplication: `grep -rn "<distinctive snippet>"`; 3rd occurrence = abstract.
- Output: `SMELL | REFACTORING | lines/CC before→after | tests (total/green)`.
