---
name: rust-async-safety
description: Review checklist for Rust services, edge collectors and FFI crates: error handling, async/tokio pitfalls, concurrency, unsafe/FFI boundaries, memory and dependency hygiene. Use when writing or reviewing Rust code, especially async, networked, protocol or FFI code.
---
# Errors and API
- `Result` with a typed error (`thiserror`; `anyhow` only at binaries' edges); no `unwrap`/`expect`/indexing panics on external input; `#[must_use]` on results that matter; never swallow I/O errors; add context at boundaries.
- Make illegal states unrepresentable (enums, newtypes, builders); `#[non_exhaustive]` for public enums that will grow.

# Async (tokio)
- Never block the runtime: CPU/blocking I/O → `spawn_blocking`/dedicated thread; no `std::sync::Mutex` guard held across `.await` (use a short critical section or `tokio::sync::Mutex`); no `block_on` inside async.
- **Cancellation safety**: every `select!` branch and `.await` point may be dropped; keep state consistent on drop; use `CancellationToken` for graceful shutdown and join tasks (no leaked `spawn`).
- Bounded channels everywhere; define overflow behavior; `JoinSet` for structured concurrency; handle task panics (`JoinError`).
- Timeouts on all I/O (`tokio::time::timeout`); reconnect with backoff + jitter (`resilience-patterns`).

# Concurrency and data
- `Send`/`Sync` bounds explicit; prefer message passing; no `static mut`; minimal `Arc<Mutex<_>>`; atomics with justified `Ordering`.
- Avoid clones/allocations in hot loops (`Bytes`, slices, `Cow`); pre-size collections; measure (`performance-profiling`).

# Unsafe and FFI
- Every `unsafe` block has a `// SAFETY:` invariant comment; smallest possible scope; wrap in a safe API.
- FFI: `#[repr(C)]`, no panic across the boundary (`catch_unwind` → error code), clear ownership (create/free pair), validate pointers/lengths, UTF-8 + explicit length for strings, test with leak/stress loops; Miri/loom for unsafe or lock-free code.

# Hygiene
`cargo fmt --check` · `cargo clippy --all-targets -- -D warnings` · `cargo test` · `cargo audit`/`cargo deny` (advisories, licenses) · minimal features and dependencies · reproducible `Cargo.lock` for binaries · no secrets in logs; `zeroize` for key material.

# Output (≤15 lines)
`FILE:LINE | issue class (error/async/concurrency/unsafe/perf/hygiene) | failure scenario | fix`.
