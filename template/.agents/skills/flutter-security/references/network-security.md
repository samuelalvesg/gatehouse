# Network Security

## HTTPS Only

- Every base URL starts with `https://`. Reject a configuration that does not.
- Do not set `badCertificateCallback` (or the equivalent) in release builds.
- A debug-only bypass is allowed for local development. It must be guarded by `kDebugMode`, and the project's known-issues list must record it.

## Certificate Pinning (decision pending)

Pinning is not required by this skill. If a product adopts it, record the decision, the pinned keys and the rotation plan in the project's documentation before changing the client.

## Sensitive Headers

Mobile HTTP clients send the `Authorization` header and nothing else for security purposes. Browser-only headers (for example `X-Frame-Options`) do not apply to a mobile app.
