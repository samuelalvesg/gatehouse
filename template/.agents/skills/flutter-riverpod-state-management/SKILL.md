---
name: flutter-riverpod-state-management
description: Manage reactive state with Riverpod in Flutter: provider scope, Notifier and AsyncNotifier, ref.watch/ref.read/ref.listen rules, async state with AsyncValue, and provider overrides in tests. Use when defining or consuming providers, or overriding them in tests.
metadata:
  triggers:
    files:
    - '**_provider.dart'
    - '**_providers.dart'
    - '**_notifier.dart'
    keywords:
    - riverpod
    - ProviderScope
    - ConsumerWidget
    - Notifier
    - AsyncNotifier
    - AsyncValue
    - ref.watch
    - ref.listen
    - overrideWithValue
---
# Riverpod State Management

## **Priority: P0 (CRITICAL)**

## Structure

```text
lib/
├── <feature>/
│   ├── <feature>_providers.dart   # providers for the feature, one file
│   └── <feature>_notifier.dart    # Notifier / AsyncNotifier classes
└── core/providers/                # providers shared by features
```

Keep providers global (top-level). Do not create providers inside widgets or inside another provider's `build`.

## Implementation Guidelines

- **Provider kinds**: a `Notifier`/`AsyncNotifier` for state that changes over time; a plain `Provider` for a dependency (repository, client, clock).
- **Async state**: model loading, data and error with `AsyncValue`, and render it with `when` or `switch` on the state.
- **`ref.watch`** inside `build()` to rebuild when a dependency changes.
- **`ref.listen`** inside `build()` for side effects (navigation, dialogs, snackbars). Never run side effects in a provider's `build`.
- **`ref.read`** only in callbacks (`onPressed`, a method of a notifier). Never in `build()`.
- **Mutations** update state through a notifier method. After a remote write, refresh with `ref.invalidateSelf()` or set the new state.
- **Immutable state**: state objects are immutable; use `copyWith` or a sealed class for variants.
- **Tests**: build a `ProviderContainer` or a `ProviderScope` with `overrides`, and override the dependency with a fake (`overrideWithValue`). Do not override the provider under test.

## Anti-Patterns

- **No side effects in `build`**: use `ref.listen` in the widget.
- **No `BuildContext` in notifiers or providers**: pass the data the notifier needs, not the context.
- **No provider created inside a widget or a `build`**: it is recreated on every build.
- **No `ref.read` inside `build`**: it will not update when the value changes.
- **No mutable state shared across notifiers**: expose state through providers, not through globals.

## Reference & Examples

See [references/implementation.md](references/implementation.md) for a notifier with `AsyncValue` and a consumer widget.

## Related Topics

- Layering rules: `.agents/rules/frontend-clean-code-rule.md`.
- Tests with mocks: the Flutter section of `test-strategy`.
- Navigation from state changes: `flutter-go-router-navigation`.
