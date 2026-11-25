---
name: flutter-go-router-navigation
description: Declare routes, shell tabs, redirects and guards with go_router in a multi-package Flutter app. Use when adding a route, a tab branch, a redirect or a guard, or when a route resolves to the wrong screen.
metadata:
  triggers:
    files:
      - "**/*routes*.dart"
      - "**/router*.dart"
      - "**/*route_guard*.dart"
    keywords:
      - GoRouter
      - GoRoute
      - StatefulShellRoute
      - redirect
      - route guard
---

# go_router Navigation

## **Priority: P0 (CRITICAL)**

## Structure

```text
<app>/lib/core/routing/
└── router_provider.dart      # builds the one GoRouter, wires redirect and onException

<core package>/lib/src/routing/
└── route_guard.dart          # pure decision: input -> redirect or allow (no BuildContext)

<feature package>/lib/src/
└── routes.dart               # pillar<Feature>Routes(): the feature's GoRoute / StatefulShellBranch list
```

Each feature package exports its routes from one function (`<feature>Routes()`). The app composes those lists in one place. A feature does not build its own `GoRouter`.

## Implementation Guidelines

- **One router.** One `GoRouter` built in the app's routing provider. Do not create routers in features.
- **Feature routes.** Each feature returns its `GoRoute` list or `StatefulShellBranch` list from `routes.dart`.
- **Tabs.** Use `StatefulShellRoute` with one branch per tab so each tab keeps its own stack.
- **Redirects.** The decision is a pure function in the core package (`resolveRouteRedirect`-style: input in, redirect or null out). The `redirect:` callback in the router is a thin adapter that reads state and calls it. The decision is unit-tested without `BuildContext`.
- **Unknown locations.** Handle them in `onException` and send the user to a safe route.
- **Navigation calls.** Use the path constants declared by the feature, not literals repeated across screens.
- **Transitions.** Keep page transitions in the feature's route builder, not in widgets.

## Anti-Patterns

- **No auth checks in widgets**: the decision lives in the redirect path.
- **No second `GoRouter`** in a feature package or in a test helper that ships with the app.
- **No decision logic inside the `redirect:` callback**: move it to the pure guard so it can be tested.
- **No route paths typed by hand in several screens**: keep them in one constants file per feature.

## Typed routes (not used here)

`GoRouteData` with `@TypedGoRoute` is supported by go_router and is described in [references/typed-routes.md](references/typed-routes.md). The project does not use it today: adopting it is a decision for the whole app, not for one feature.

## Related Topics

- Guard logic and its tests: the `test-strategy` skill, Flutter section.
- Package boundaries: the `pacote-folha` skill.
