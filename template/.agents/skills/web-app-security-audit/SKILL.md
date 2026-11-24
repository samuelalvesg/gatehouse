---
name: web-app-security-audit
description: Pre-launch security audit of a web app (API routes, auth, uploads, webhooks, client bundles, database policies) as a fixed PASS/FAIL/N/A/NOT VERIFIED table with severities and fixes. Use before release or when a reviewer or the security agent must check a web app.
---

# Web app security audit

Read the code, database policies and configuration. Do not guess. An item the repository cannot show is `NOT VERIFIED`, with what is missing. Generic code review (injection, crypto, dependencies): `owasp-sanitizer`.

## Output

One table, then the fixes.

| ID | Check | Status | Severity | Evidence (`file:line`) | Fix |
|---|---|---|---|---|---|

- Status: `PASS`, `FAIL`, `N/A` (stack or feature absent), `NOT VERIFIED`. Severity for `FAIL`: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`; otherwise `-`.
- After the table: file path and exact fix for every `CRITICAL` or `HIGH` `FAIL`.
- Run `scripts/security/scan_web_patterns.py` first. Confirm each hit by reading the file; a scanner `PASS` is not a verdict.

## A. Secrets and environment
- **A1** No service keys, private tokens or passwords in public variables (`NEXT_PUBLIC_*`, `VITE_*`, client bundles).
- **A2** `.env` files are git-ignored; development and production values are separate.

## B. Data access (any database)
- **B1** Tables with user data have row-level access control scoped to the user or tenant.
- **B2** No policy grants anonymous (`anon`) read or write on sensitive tables.
- **B3** Users cannot change their own role or privileges via profile update or client query.
- **B4** Server queries filter by the authenticated session, not by a client-sent ID.
- **B5** Elevated-rights database functions check the caller and set a fixed search path.
- **B6** Public queries do not return sensitive fields (personal data, tokens).
- **B7** The app's database role has least privilege; no superuser or owner role in app configuration.

## C. Storage and uploads
- **C1** Buckets are private unless public is intended.
- **C2** Sensitive files use short-lived signed URLs, not predictable public paths.
- **C3** Uploads check content type, size limits and path traversal.

## D. Authentication and authorization
- **D1** Protected pages and API routes check the session on the server.
- **D2** Server actions check session and permission before changing data.
- **D3** Authorization does not rely only on middleware or the frontend.
- **D4** The framework version is patched against known middleware-bypass issues. Check the version against the vendor advisory; do not assume.
- **D5** IDOR: changing an ID in a request cannot read or change another user's data. Test one case.
- **D6** Admin rights are checked on the server and in the database, not only in the UI.
- **D7** Hidden UI elements are not the only protection.

## E. Endpoints, webhooks and infrastructure
- **E1** No forgotten debug, test or unprotected admin routes in the build.
- **E2** Scheduled endpoints require a secret header.
- **E3** Incoming webhooks verify the signature before acting.
- **E4** CORS does not combine a wildcard origin with credentials or private data.

## F. Session and auth hardening
- **F1** The auth secret is strong and server-only.
- **F2** Session cookies set `HttpOnly`, `Secure` and `SameSite`.
- **F3** Email verification is required; open sign-up is a deliberate choice.
- **F4** Password policy rejects known-leaked passwords.
- **F5** MFA is available and required for privileged accounts.
- **F6** Sessions expire and refresh tokens rotate.
- **F7** Password recovery does not reveal whether an email exists.
- **F8** State-changing routes have CSRF protection unless they use same-site tokens.

## G. Rate limiting and abuse
- **G1** Login, sign-up and password recovery are rate-limited.
- **G2** Routes that call paid APIs have rate limits and spend caps, per user and global.
- **G3** Public forms and unauthenticated endpoints have rate limits or a CAPTCHA.
- **G4** Password hashing is memory-hard and bounded. Each hash or verify call uses a fixed, reviewed memory cost, and the number of concurrent hashing operations is capped (semaphore, queue or worker pool). Without a cap, N parallel logins allocate N times the memory cost (for example 64 MiB each).
- **G5** Login, token refresh and password recovery are rate-limited per account and per IP, both by a limiter on the endpoint and, where possible, at the edge. Check the attribute on every login route, including minimal-API handlers. Not verified if the edge configuration is not in the repository.
- **G6** An unknown user and a wrong password take comparable time: the hash runs (or a dummy hash runs) on the unknown-user path, so response time does not reveal which accounts exist.
- **G7** Password length has a maximum (for example 128 or 256 characters) and the route's body size limit is below the framework default.
- **G8** The client IP used for rate limits is trusted only when the connection comes from a known proxy or the edge provider's published ranges. Headers such as `CF-Connecting-IP`, `X-Forwarded-For` and `X-Real-IP` are read only after that check, and forwarded-header options do not clear the known-proxy lists. Without this, an attacker sends a new IP header on each attempt and bypasses every per-IP limit. When the edge is part of the design, check that the origin accepts traffic only from it.
- **G9** Login protection escalates: a high global ceiling, per-account and per-IP sliding windows, a CAPTCHA or managed challenge after a few failures (for example 5), and growing delays. A temporary account lock is avoided, because it lets an attacker lock out real users. The edge rule must exist in the infrastructure configuration; if it is not in the repository, mark `NOT VERIFIED`.

## H. Input and output
- **H1** Every request body and query parameter is validated on the server with a schema.
- **H2** No unsanitized HTML output (`dangerouslySetInnerHTML`, `innerHTML`, `v-html`); HTML goes through a sanitizer.
- **H3** Queries use parameters only; no string concatenation into SQL.
- **H4** Redirect targets (`callbackUrl`, `redirectTo`, `next`) accept only local paths.

## I. Outbound requests (SSRF and timeouts)
- **I1** URLs from user input are checked against a host allowlist; private, loopback and cloud-metadata addresses are refused.
- **I2** Every outbound HTTP call sets a timeout.
- **I3** Retries apply only to idempotent calls, with a limit and backoff.

## J. Tokens and cryptography
- **J1** Tokens are verified, not only decoded; accepted algorithms are fixed and `none` is refused.
- **J2** Access tokens expire within a short window; refresh tokens can be revoked.
- **J3** Signing keys rotate without a deploy, and old keys stop working after rotation.
- **J4** TLS is enforced end to end; `Strict-Transport-Security` is set on the public host.
- **J5** Sensitive fields at rest are encrypted, or the choice is documented.
- **J6** Passwords, tokens and secrets never reach logs, error messages or analytics.
- **J7** Hash parameters read from storage (memory, iterations, parallelism) are checked against fixed bounds; out-of-bound values are rejected, not trusted.

## K. OAuth and third-party sign-in
- **K1** The authorization request uses `state`, and PKCE for public clients.
- **K2** The redirect URI is matched exactly against a registered list.

## L. Money, state and concurrency
- **L1** Payment and webhook handlers are idempotent: a repeated event does not charge or grant twice.
- **L2** Changes that depend on a previous read use a transaction, a conditional update or optimistic locking.
- **L3** Check-then-act sequences are protected against two concurrent requests.

## M. Errors and response headers
- **M1** Client error responses carry no stack traces, SQL text or internal paths.
- **M2** The public host sends a Content-Security-Policy and the usual security headers (`X-Content-Type-Options`, `Referrer-Policy`, frame protection).
- **M3** Debug mode and verbose errors are off in production configuration.

## N. Dependencies and data lifecycle
- **N1** Known-vulnerable dependencies are checked with the ecosystem's audit tool (`npm audit`, `pip-audit`, `cargo audit`, `dotnet list package --vulnerable`) and the result is recorded. `NOT VERIFIED` if the tool did not run.
- **N2** Destructive migrations (drop, type change that loses data) are reviewed and have a rollback path.
- **N3** Backups exist and have been restored at least once. This cannot be seen in the repository: mark `NOT VERIFIED` unless there is evidence.

## Stack modules (only when the stack is present)
- **Supabase or Firebase:** B1, B2 and C1 are checked against policy files and migrations, not only client code; Firebase: the security rules file.
- **Next.js:** D1–D3 are checked separately in middleware, route handlers and server actions.
