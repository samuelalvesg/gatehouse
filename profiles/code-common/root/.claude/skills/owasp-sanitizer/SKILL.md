---
name: owasp-sanitizer
description: Audits code and dependencies against OWASP Top 10 vulnerabilities, insecure defaults, sanitization flaws, authentication bypasses, and secret leaks.
---
# Security Checklist
1. **Injection (SQL, Command, LDAP, NoSQL)**:
   - Ensure parameterized queries and ORM abstractions. Reject string interpolation in SQL/raw commands.
2. **Broken Authentication & Authorization**:
   - Verify role-based/claims-based authorization on every route. Prevent horizontal privilege escalation (tenant/user ID checks).
3. **Sensitive Data Exposure & Secret Leaking**:
   - Verify no hardcoded API keys, JWT secrets, passwords, or tokens in source code or Git history. Ensure sensitive fields are masked in logs.
4. **Security Misconfiguration**:
   - Verify CORS policies, secure cookie attributes (HttpOnly, Secure, SameSite), CSRF tokens, and security headers (CSP, HSTS).
5. **Vulnerable and Outdated Dependencies**:
   - Audit lockfiles for known CVEs using package managers (`dotnet list package --vulnerable`, `npm audit`, `cargo audit`).
6. **Input Validation & Output Encoding**:
   - Validate input format, length, and types at system boundaries. Encode HTML output to prevent XSS.

# Report Format
`# | vulnerability | component:line | OWASP Category | risk (Critical/High/Medium/Low) | remediation`

# Additional guidance
Principle: validate at the **edge** (allow-list), encode on **output** (by context), always parameterize; never trust client, header, file name, or a tenant id from the request.

| # | Check | How |
|---|---|---|
| A01 Access | every new Controller has `[Authorize]`/policy; tenant comes from the token, not the body; IDOR: resource belongs to tenant/user | `grep -rn "class .*Controller" <backend>`; check attribute and tenant filter |
| A02 Crypto | no MD5/SHA1 for passwords; strong password hash (Argon2id/bcrypt/scrypt); no key/secret in code; TLS | `grep -rniE "md5\|sha1\|DES\|ECB" <backend>` |
| A03 Injection | parameterized SQL/LINQ only; no `FromSqlRaw($"...")`/concatenation; no `Process.Start` with input; no `Path.Combine` with a user name unnormalized | `grep -rnE "FromSqlRaw\|ExecuteSqlRaw\|string\.Format.*SELECT\|\+ .*WHERE" <backend>` |
| A03 XSS | HTML/e-mail output encoded; Flutter Web: no `innerHTML`/`HtmlElementView` with untrusted data | `grep -rnE "innerHTML\|dangerouslySet\|HtmlElementView" <frontend>` |
| A04 Design | payload size, upload (type by content, not extension; zip bomb), rate limit, pagination | see `the zip-bomb audit item` |
| A05 Config | no debug/stack trace in production; CORS not `*` with credentials; headers; secrets only via env (12-Factor III) | read `Program.cs`, `appsettings*.json` (never print values) |
| A06 Components | vulnerable/abandoned dependency | `dotnet list <solution> package --vulnerable --include-transitive`; `cd <frontend> && dart pub outdated`; `cargo audit` (`command -v cargo-audit`) |
| A07 Authentication | no hardcoded credential; expiry/refresh; lockout; constant-time comparison | `grep -rniE "password\s*=\s*\"\|apikey\|secret\s*=\s*\"" --include=*.cs --include=*.dart --include=*.rs .` |
| A08 Integrity | webhook signature verified; deserialize expected types only (no `TypeNameHandling`) | `grep -rn "TypeNameHandling\|BinaryFormatter" <backend>` |
| A09 Logging | no secret/PII/token in logs; denied-authz events logged | review `ILogger` calls in the diff |
| A10 SSRF | user-supplied URL: host allow-list, block internal IP/metadata | `grep -rn "HttpClient" <backend>` + URL origin |

Rules of thumb: input = type → size → format → allow-list → only then use (reject > "clean"). SQL: `@param`/LINQ; dynamic identifier (column/order) via fixed allow-list map. Output: encode by context (HTML, attribute, JS, URL). User text into AI = data, not instruction (prompt injection). Errors: generic message to the client, detail only in logs. Leaked secret: stop, never print the value, report `file:line` + type, recommend rotation, never rewrite git history. Output ≤25 lines: `ID | sev (Crítica/Alta/Média/Baixa) | file:line | vector input→sink | fix`; with no findings list which A0x were checked and what stayed "not verified".
