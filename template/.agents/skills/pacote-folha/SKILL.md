---
name: pacote-folha
description: Decide where a feature lives in a multi-package Flutter/Dart monorepo, and how to split it so packages do not form dependency cycles: contract in the core package, implementation in the app or in a "leaf package" (pacote-folha), and a thin native shell for FFI. Use when creating a package, moving code between packages, or when a `pub get` cycle or a core-to-feature import appears.
metadata:
  triggers:
    files:
    - 'packages/**/pubspec.yaml'
    - 'pubspec.yaml'
    - 'lib/**/*_provider*.dart'
---
# Leaf Package (pacote-folha) and Contracts

## Why this exists
A core package (for example `pillar_core`) and an API package (for example `symmetris_api`) can each depend on the other only if the code of one lives inside the other. A **leaf package** is a third package that only consumes both and is never imported back by them. It can depend on both at the same time without breaking anything: `pub get` only rejects a cycle between the same two packages.

## Rules
1. **Pure contract → core package.** Code with no I/O and no dependency on the API package goes into `<core>/lib/src/<domain>/`: a narrow contract (one or two providers, pure types, no network, no storage). Keep the real implementation outside the core and inject it with an override (`ProviderContainer` override or `ProviderScope.overrides`).
2. **Real I/O or API dependency → leaf package.** Code that calls HTTP, native storage or FFI, or that depends on the API package, becomes a leaf package. It does not go into the core package.
3. **Check for an existing home first.** Before creating a package, look for a leaf package that already covers the same business domain. Add the code there. Split a domain across several small packages only when the domain really has no home yet.
4. **Native shell (thin FFI wrapper).** When a native library (for example a Rust core through `flutter_rust_bridge`) must be embedded, keep a thin package that only exposes the binding. The business logic stays in the library, which the shell calls and does not reimplement.
5. **Adapter for an external SDK.** A package that wraps a third-party SDK implements a contract from another package. It is the only package allowed to import that SDK. Removing the integration means deleting that package.

## Checklist for every new feature or split
1. Is the code pure and free of API dependencies? → contract in the core package (rule 1).
2. Does it need I/O or the API package? → leaf package (rule 2); first check for an existing home (rule 3).
3. Split in separate, low-risk PRs. Pure functions get automated tests before their real import is swapped. Logic that needs heavy I/O without a fake is checked with the analyzer, a manual review and a directed smoke test.
4. Done means: `flutter analyze` clean and `flutter test` without new failures, per PR, not for the whole split at once.

## Anti-patterns
- A core package that imports a feature package.
- A leaf package imported back by the core or the API package.
- A new package per small piece of one domain.
- A contract that carries an implementation detail (base URL, SDK type).

## Output
For each item to move: `ITEM | cause of the dependency | category (contract / leaf / shell / adapter / stays in app) | decision`.
