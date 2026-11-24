---
name: web-app-security-audit
description: Pre-launch security audit of a web app (API routes, auth, uploads, webhooks, client bundles, database policies) as a fixed PASS/FAIL/N/A/NOT VERIFIED table with severities and fixes. Use before release or when a reviewer or the security agent must check a web app.
---

# Web app security audit

Read the code, the database policies and the configuration. Do not guess. If an item cannot be checked from the repository, mark it `NOT VERIFIED` and say what is missing.

For generic code review (injection, crypto, dependencies) use `owasp-sanitizer`. This skill covers the web-app checklist and the output format.

## Output

One Markdown table, then the fixes.

| ID | Check | Status | Severity | Evidence (`file:line`) | Fix |
|---|---|---|---|---|---|

- Status: `PASS`, `FAIL`, `N/A` (the stack or feature is absent), `NOT VERIFIED`.
- Severity for `FAIL`: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`. Use `-` otherwise.
- After the table, list the file path and the exact fix for every `FAIL` with `CRITICAL` or `HIGH`.

Run `python3 scripts/security/scan_web_patterns.py` first. It finds the mechanical items. Confirm each hit by reading the file before you mark it `FAIL`. The scanner's `PASS` is not a verdict.

## A. Secrets and environment

- **A1** No service keys, private tokens or passwords in public variables (`NEXT_PUBLIC_*`, `VITE_*`, any client bundle).
- **A2** `.env` files are git-ignored, and development and production values are separate.

## B. Data access (any database)

- **B1** Every table that holds user data has row-level access control enabled, with policies that scope rows to the authenticated user or tenant.
- **B2** No policy grants anonymous (`anon`) read or write on sensitive tables.
- **B3** Users cannot change their own role or privileges through a profile update or a client query.
- **B4** Server-side queries filter by the authenticated session, not by an ID sent by the client.
- **B5** Database functions that run with elevated rights check the caller's permission and set a fixed search path.
- **B6** Sensitive fields (personal data, tokens) are not returned by public queries.
- **B7** The database role used by the app has the least privilege its code needs. No superuser or owner role in app configuration.

## C. Storage and uploads

- **C1** Buckets are private unless public is intended.
- **C2** Sensitive files are reached through short-lived signed URLs, not predictable public paths.
- **C3** Uploads check type by content, size limits, and path traversal.

## D. Authentication and authorization

- **D1** Protected pages and API routes check the session on the server.
- **D2** Server actions check the session and the permission before they change data.
- **D3** Authorization does not rely only on middleware or on the frontend.
- **D4** The framework version is patched against known middleware-bypass issues. Check the version against the vendor advisory; do not assume.
- **D5** IDOR: changing an ID in a request cannot read or change another user's data. Test one case.
- **D6** Admin rights are checked on the server and in the database, not only in the UI.
- **D7** Hidden buttons are not the only protection.

## E. Endpoints, webhooks and infrastructure

- **E1** No forgotten debug, test or unprotected admin routes in the build.
- **E2** Scheduled endpoints require a secret header.
- **E3** Incoming webhooks verify the signature before they act.
- **E4** CORS does not combine a wildcard origin with credentials or private data.

## F. Session and auth hardening

- **F1** The auth secret is strong and used only on the server.
- **F2** Session cookies set `HttpOnly`, `Secure` and `SameSite`.
- **F3** Email verification is required, and open sign-up is a deliberate choice.
- **F4** Password policy rejects known-leaked passwords.
- **F5** MFA is available, and required for privileged accounts.
- **F6** Sessions expire, and refresh tokens rotate.
- **F7** Password recovery does not reveal whether an email exists.
- **F8** State-changing routes have CSRF protection unless they use same-site tokens.

## G. Rate limiting and abuse

- **G1** Login, sign-up and password recovery are rate-limited.
- **G2** Routes that call paid APIs have rate limits and spend caps per user and globally.
- **G3** Public forms and unauthenticated endpoints have rate limits or a CAPTCHA.

## H. Input and output

- **H1** Every request body and query parameter is validated on the server with a schema.
- **H2** No unsanitized HTML output (`dangerouslySetInnerHTML`, `innerHTML`, `v-html`). If HTML is needed, it goes through a sanitizer.
- **H3** Queries use parameters only. No string concatenation into SQL.
- **H4** Redirect targets (`callbackUrl`, `redirectTo`, `next`) accept only local paths.

## I. Outbound requests (SSRF and timeouts)

- **I1** A URL taken from user input is checked against an allowlist of hosts, and private, loopback and cloud-metadata addresses are refused.
- **I2** Every outbound HTTP call sets a timeout.
- **I3** Retries apply only to idempotent calls, with a limit and a backoff.

## J. Tokens and cryptography

- **J1** Tokens are verified, not only decoded. The accepted algorithms are fixed, and `none` is refused.
- **J2** Access tokens expire within a short window, and refresh tokens can be revoked.
- **J3** Signing keys can be rotated without a deploy, and old keys stop working after rotation.
- **J4** TLS is enforced end to end, and `Strict-Transport-Security` is set on the public host.
- **J5** Sensitive fields at rest (tokens, personal identifiers) are encrypted, or the choice is documented.
- **J6** Passwords, tokens and secrets are not written to logs, error messages or analytics.

## K. OAuth and third-party sign-in

- **K1** The authorization request uses `state` and, for public clients, PKCE.
- **K2** The redirect URI is matched exactly against a registered list, not by prefix or pattern.

## L. Money, state and concurrency

- **L1** Payment and webhook handlers are idempotent: a repeated event does not charge or grant twice.
- **L2** A balance, quota or state change that depends on a previous read uses a transaction, a conditional update, or optimistic locking.
- **L3** A check followed by an action (check-then-act) is protected against two requests running at once.

## M. Errors and response headers

- **M1** Error responses to clients carry no stack traces, SQL text or internal paths.
- **M2** The public host sends a Content-Security-Policy and the usual security headers (`X-Content-Type-Options`, `Referrer-Policy`, frame protection).
- **M3** Debug mode and verbose errors are off in the production configuration.

## N. Dependencies and data lifecycle

- **N1** Known-vulnerable dependencies are checked with the ecosystem's audit tool (`npm audit`, `pip-audit`, `cargo audit`, `dotnet list package --vulnerable`), and the result is recorded. Not verified if the tool did not run.
- **N2** Destructive migrations (drop column, drop table, type change that loses data) are reviewed and have a rollback path.
- **N3** Backups exist and have been restored at least once. This cannot be seen in the repository: mark `NOT VERIFIED` unless there is evidence.

## Stack modules (apply only when the stack is present)

- **Supabase or Firebase:** B1–B2 and C1 are checked against the policy files and the migrations, not only the client code. Firebase: check the security rules file.
- **Next.js:** check D1–D3 in middleware, route handlers and server actions separately.
