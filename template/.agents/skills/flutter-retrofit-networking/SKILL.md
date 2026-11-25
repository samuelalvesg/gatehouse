---
name: flutter-retrofit-networking
description: Build typed HTTP networking with Dio in Flutter: remote datasources, JSON DTOs with tolerant enums, auth header injection, one-retry token refresh on 401, and mapping of Dio errors to typed failures. Use when adding or changing a remote API call, an auth interceptor, or a DTO.
metadata:
  triggers:
    files:
    - '**/data_sources/**'
    - '**/api/**'
    - '**/*_remote_datasource.dart'
    - '**/*_http_client.dart'
    keywords:
    - Dio
    - Interceptor
    - InterceptorsWrapper
    - QueuedInterceptorsWrapper
    - DioException
    - 401
    - unknownEnumValue
---
# Dio Networking

## **Priority: P0 (CRITICAL)**

## Structure

```text
<api package>/lib/src/
├── <domain>/
│   ├── <name>_remote_datasource.dart   # Dio calls, returns DTOs
│   └── <name>_repository.dart          # maps DTOs to domain entities, maps errors to failures
└── http/
    └── <client>_http_client.dart       # one Dio instance with interceptors
```

## Implementation Workflow

1. **One Dio client per app.** Build it in one place with `BaseOptions` (base URL, timeouts, `Content-Type`). Inject it; never call `Dio()` inside a datasource or a screen.
2. **Remote datasource per resource.** A class that takes `Dio` in its constructor and returns DTOs. Keep path strings in that class, not in screens.
3. **DTOs with `json_serializable`.** Use `fromJson`/`toJson` generated code. For each enum that the backend may extend, add `@JsonKey(unknownEnumValue: <Enum>.unknown)` so a new value does not crash parsing.
4. **Repository maps DTOs to entities** and maps `DioException` to typed failures (network, server, unauthorized). Screens never see `DioException`.
5. **Auth header** is added in `onRequest`, from the token provider the client receives. No token is read from a global variable.
6. **401 refresh with one retry.** On 401, call the refresh hook once, then repeat the original request with the new token. Mark the repeated request (for example in `RequestOptions.extra`) so a second 401 does not loop.
7. **Concurrent 401s.** Use `QueuedInterceptorsWrapper` so that requests failing together wait for one refresh instead of starting several.

## Anti-Patterns

- **No `Dio()` per call**: inject one client.
- **No manual JSON parsing in screens**: generated `fromJson` only.
- **No unguarded enums**: always set `unknownEnumValue` on enums that the backend may extend.
- **No `DioException` above the repository**.
- **No retry loop on 401**: retry once, then fail.

## Reference & Examples

See [references/implementation.md](references/implementation.md) for a datasource, a tolerant enum DTO and the error mapping, and [references/token-refresh.md](references/token-refresh.md) for the refresh interceptor.

## Related Topics

- Layering rules: `.agents/rules/frontend-clean-code-rule.md`.
- Failure types and error handling: `dotnet-flutter-hotspots` (Flutter section).
- Secure storage of tokens: `flutter-security`.
