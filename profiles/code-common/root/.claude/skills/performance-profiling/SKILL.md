---
name: performance-profiling
description: Measures and improves performance across C#, Rust and Flutter: define a budget, profile before changing, optimize the hot path, prove the gain with a repeatable benchmark/load test. Use for latency/throughput/memory/startup/frame-time work or before claiming an optimization.
---
# Rule
No optimization without a **budget** (p95/p99, throughput, memory, frame time, startup) and a **before/after measurement** on a repeatable workload. "Faster" without numbers is "not measured".

# Method
1. State the workload and budget (e.g. ingest N samples/s at p99 < X ms on this hardware).
2. Measure baseline, same machine, warmed up, release build, N runs; record variance.
3. Profile to find the real hot spot (do not guess): sampling profiler first, then targeted counters/allocation tracking.
4. Change **one** thing; re-measure; keep it only if the gain exceeds noise and no budget regresses (memory, tail latency, readability).
5. Add a regression guard (benchmark threshold, allocation test, query-count assertion) where it is cheap and stable.

# Tools
- **C#/.NET**: `BenchmarkDotNet` (micro), `dotnet-counters`/`dotnet-trace`/`dotnet-gcdump`, EF query count + `EXPLAIN` (`query-performance-tuner`), avoid LINQ/closures/boxing/`string` concat in hot paths, `Span<T>`/`ArrayPool`, `ValueTask`, async all the way (no sync-over-async), `Channel<T>` for pipelines, `System.Text.Json` source generators, avoid GC pressure from per-item allocation.
- **Rust**: `cargo bench` with `criterion`, `cargo flamegraph`/`perf`, allocation counters (`dhat`), release profile (`opt-level`, `lto`, `codegen-units`), avoid cloning/allocating in loops, prefer iterators/slices, batch I/O, bounded channels; async: do not block the runtime (use `spawn_blocking`), avoid holding locks across `.await`.
- **Flutter/Dart**: DevTools Performance/CPU/Memory in **profile mode** (never debug), 16 ms/8 ms frame budget, `const` widgets, narrow rebuilds (selectors), `RepaintBoundary` for animated/heavy subtrees, lists with builders and stable keys, heavy work in isolates/Rust via FFI, image sizing/caching, avoid `setState` per message for live data (batch per frame).
- **Load/soak**: `k6`/`bombardier`/custom replay for services; soak tests for leaks (memory/handles/connections stable over hours).

# Anti-patterns
Benchmarking debug builds · measuring once · optimizing cold paths · caching without invalidation/limits · unbounded queues "for throughput" · trading correctness or safety for speed without sign-off.

# Output (≤15 lines)
`WORKLOAD | budget | baseline | change | after | method/tool | risk | guard`.
