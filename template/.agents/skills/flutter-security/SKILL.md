---
name: flutter-security
description: Protect tokens, personal data and secrets in a Flutter app: secure storage, build-time configuration with --dart-define, obfuscated release builds, PII masking in logs, and HTTPS-only networking. Use when storing credentials, handling personal data, configuring builds, or reviewing a release.
metadata:
  triggers:
    files:
    - '**/*_local_datasource.dart'
    - '**/*_storage*.dart'
    - 'pubspec.yaml'
    - '**/*_http_client.dart'
    keywords:
    - flutter_secure_storage
    - SharedPreferences
    - dart-define
    - obfuscate
    - PII
    - token
---
# Mobile Security

## **Priority: P0 (CRITICAL)**

## Implementation Workflow

1. **Tokens and personal data** go in `flutter_secure_storage`. Never in `shared_preferences`, plain files or logs.
2. **Secrets are not in Dart code.** Pass them at build time with `--dart-define` (for example, the API base URL). Keep signing keys and service credentials out of the repository.
3. **Release builds** use `--obfuscate --split-debug-info=<folder>` and keep the symbol files out of the repository. Obfuscation is a deterrent, not a control: keep sensitive rules on the backend.
4. **Mask PII in logs.** Log identifiers, not e-mails, phones, documents or tokens. Check analytics events the same way.
5. **HTTPS only.** Every base URL uses `https`. Certificate validation is never disabled outside debug builds, and a debug-only bypass is marked in code and in the docs.

Decisions that are not part of this skill and must be made per product: certificate pinning, and root or jailbreak detection. Record the decision in the project before adding either one.

## Reference & Examples

See [references/implementation.md](references/implementation.md) for secure storage and the release build command, and [references/network-security.md](references/network-security.md) for HTTPS and certificate rules.

## Anti-Patterns

- **No secrets in `shared_preferences`**: use secure storage.
- **No hardcoded keys or URLs with credentials**: use `--dart-define`.
- **No unobfuscated release builds**.
- **No PII in logs or analytics**.
- **No certificate validation switched off in release builds**.

## Related Topics

- Token refresh and the auth interceptor: `flutter-retrofit-networking`.
- Backend and OWASP review: `owasp-sanitizer`.
