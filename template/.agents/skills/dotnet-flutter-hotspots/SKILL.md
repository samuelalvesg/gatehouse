---
name: dotnet-flutter-hotspots
description: Review checklist of frequent defects in C#/.NET services and Flutter/Dart apps: async misuse, EF Core pitfalls, DI lifetimes, cancellation, disposal, state management, rebuild/stream leaks, offline/sync. Use when reviewing or writing C# backend code or Flutter code.
---
# C# / .NET
- **Async**: async all the way; no `.Result`/`.Wait()`; `CancellationToken` as last parameter and passed down; `ConfigureAwait(false)` in libraries; no `async void` except event handlers; don't fire-and-forget without error handling (use hosted services/queues).
- **Disposal/lifetimes**: `IHttpClientFactory` (no `new HttpClient()` per call); scoped services not captured by singletons; `IAsyncDisposable`; `using` for streams/connections.
- **EF Core**: `AsNoTracking` for reads; project to DTOs; avoid N+1 (`Include`/batch); no `ToList()` before filtering; keyset pagination; explicit transactions for multi-step writes; migrations reviewed, defaults for new non-null columns/collections; concurrency tokens for contended rows; no lazy loading surprises. See `query-performance-tuner`.
- **Layering**: application services free of HTTP types; exceptions as contract; validation at the edge; no static mutable state; DI over `new`.
- **Hot paths**: avoid LINQ/allocations/boxing/string concat; `Span<T>`, `ArrayPool`, `ValueTask`, source-generated JSON/logging; `Channel<T>` pipelines with bounded capacity.
- **Security/resilience**: parameterized queries, authz on every endpoint, secrets from config/env, timeouts + retries via resilience pipelines (`resilience-patterns`).

# Flutter / Dart
- **State**: single owner per piece of state; Riverpod providers scoped and disposed (`autoDispose` where appropriate), no logic in `build()`, no `BuildContext` across async gaps (check `mounted`), immutable models.
- **Streams/timers**: cancel subscriptions/timers/controllers in `dispose`; avoid multiple listeners on single-subscription streams; for high-rate data batch per frame and keep last value per key.
- **Rebuilds**: `const` constructors, narrow selectors, split widgets, builders with keys for lists, `RepaintBoundary` for heavy paint; profile in profile mode (`performance-profiling`).
- **Async/UI**: show loading/empty/error/offline states; never `await` heavy work on the UI isolate (use isolates or Rust FFI); handle every `Future` error.
- **Offline/sync**: local DB as source of truth (Drift), queue writes with idempotency keys, conflict policy written down, visible sync state; request errors → fallback, never crash.
- **Platform/FFI**: generated bindings regenerated not edited; web vs native conditional imports; permissions and lifecycle handled.
- **Tests**: widget tests for the 5 states, provider tests with overrides, golden tests only for stable UI, integration test that the app starts (cold start + native core responds).

# Output (≤15 lines)
`FILE:LINE | area | issue | failure scenario | fix`.
