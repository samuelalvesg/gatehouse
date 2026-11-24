# 0002 - A leaf package breaks a dependency cycle

**Status:** Example

## Context

Package A holds a shared contract. Package B holds the API client and depends on A. Moving the feature that needs both into A would create the cycle A → B → A, which the package manager refuses.

## Decision

1. Code that needs both A and B lives in a new leaf package C. Nothing imports C except the application.
2. A holds only a narrow contract: one or two interfaces, pure types, no I/O, no dependency on B. The implementation of the contract lives in the application and is injected.
3. Before creating a leaf package, check whether one already exists for the same domain. Reuse it, so one domain has one home.
4. Use the checklist: does the code need I/O or the client? If not, it is a contract in A. If yes, it is a leaf package.

## Consequences

- The cycle cannot come back: C is imported by no one in A or B.
- A stays small, so changing it does not force changes in every feature.
- One more package to maintain. The domain check in step 3 keeps it from multiplying.
