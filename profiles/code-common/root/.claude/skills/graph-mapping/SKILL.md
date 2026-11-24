---
name: graph-mapping
description: Maps dependencies and blast radius (callers, dependents) before modifying code. Uses graphify if installed, otherwise grep/AST analyzers.
---

# Objective
Answer with concrete evidence: **What breaks or changes if I modify X?** Without scanning the entire repository arbitrarily.

# Steps
1. **Target**: target symbol, file, or endpoint.
2. **Graphify (preferred if `graphify` is present in PATH or `graphify-out/`)**: query the dependency graph. Never install packages without user request.
3. **Fallback by layer**:
   - C#: `grep -rn "TypeName" <backend-dir> --include=*.cs` (usages, interfaces, DI registrations in `AddScoped/AddTransient`), controllers for routes, event handlers.
   - Dart: `grep -rn "import .*filename"` and package `dart analyze`.
   - Rust: `grep` across crates, `cargo tree -i <crate>`.
   - Docs: `grep -rn "<term>" docs/` to find canonical documentation owners.
4. **Classify edges**: direct caller, transitive caller (max 2 hops), test coverage, DI/config, external contract (app, webhooks).
5. **Flag boundary crossings**: module, tenant boundary, backend <-> frontend, submodules.

# Output (<= 30 lines)
```
TARGET: <symbol>
DIRECT: path:line ...
TRANSITIVE: ...
COVERING TESTS: ...
EXTERNAL CONTRACT: yes/no (details)
RISK: low|medium|high + rationale
NOT VERIFIED: ...
```

# Rules
- Report only observed facts. Dynamic reflection or unregistered DI without tests -> state "not verified".
- Stop once the blast radius is bounded.

# Additional guidance
- Prefer `graphify` if on PATH or `graphify-out/` exists (`command -v graphify`); never install it unasked.
- C#: `grep -rn "TypeName" <backend> --include=*.cs` (usages, `: IInterface`, DI registrations `AddScoped/AddTransient`), `Controllers/` for routes, CAP/SignalR handlers for events. Dart: `grep -rn "import .*file"`, `dart analyze` of the touched package, owner in `<frontend>/packages/`. Rust: `grep` in `rust_crates/`, `cargo tree -i <crate>`. Docs: `grep -rn "<term>" docs/`.
- Classify edges: direct caller · transitive caller (max 2 hops) · test · config/DI · external contract (app, edge gateway, webhook). Mark boundary crossings: module, tenant, backend↔frontend, submodule.
- Output (≤30 lines): `ALVO / DIRETOS / TRANSITIVOS / TESTES QUE COBREM / CONTRACT EXTERNO / RISCO / NOT VERIFIED`. Dynamic dependencies (reflection, convention DI) not covered → "not verified". Stop when the radius closes.
