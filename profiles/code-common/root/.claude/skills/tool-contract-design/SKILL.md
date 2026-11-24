---
name: tool-contract-design
description: Designs reliable, safe, and robust tool contracts (MCP / CLI tools) with explicit input schemas, strict validation, and structured error responses.
---
# Contract Design Principles
1. **Explicit Schemas**: Use JSON Schema / strong types for all inputs and outputs.
2. **Deterministic Inputs**: Require explicit paths or IDs; reject ambiguous wildcard or freeform prompts where precise inputs are expected.
3. **Idempotency**: Tools performing state changes must support idempotency or return clear current-state indicators.
4. **Structured Error Handling**: Return actionable error codes and failure explanations, not unhandled stack traces or generic 500s.
5. **Least Privilege & Security**: Sanitize path parameters against path traversal (`../`); prevent arbitrary shell evaluation.

# Contract Structure
- **Tool Name**: Verb-Noun identifier (e.g. `get_database_schema`, `run_query`).
- **Input Parameters**: Type, description, default value, required status.
- **Output Schema**: JSON structure or exact return format.
- **Error Conditions**: Expected failure modes and corresponding error responses.

# Additional guidance
- Everything is a single contract consumed by any wrapper (app, CLI, AI, SignalR/gRPC); business rules live in the Application Service, wrappers only translate. Start from the question the consumer wants answered; `grep` for an existing contract first.
- Contract sheet: `id` (verb + object, stable, e.g. `list_events`) · `summary` (1 line; for a light model such as a small local model the name and summary **are** the documentation) · `parameters` (few; **names, not ids** for the AI; closed types; validated schema) · `effect` **L**ookup · **R**eversible · **E** irreversible/external write (E goes through an approval queue; the AI has **no "delete"**) · `requires` (permission/role/tenant; missing permission = structured error) · `result` (typed fields, never decide by Portuguese text; summary first + `offset`/`limit` pagination; AI data in TOON) · `coverage` (what was examined/truncated; partial results flagged) · `error` (stable code + cause + what to do) · `idempotency` (repeated write does not duplicate; key).
- Limits only where a real constraint exists; compute expansion before allocating. Versioned contract; incompatible change = backend first + app plan. New capability with open effect/authority/scope → do not integrate (fail-closed), ask the user. Honest effect declaration. Never patch a contract defect with skill/prompt text. A new AI tool is born in the **backend**; the app's tools are never removed.
- Verification: contract (schema), permission/tenant, partial-result and error tests; check that name/summary suffice for a light model. Output: filled sheet + contract delta (ADDED/MODIFIED/REMOVED) for the `@architect` handoff.
