# Dio Reference

- Client, datasource, DTO and repository layers: see `SKILL.md`.
- Concrete examples: `implementation.md`.
- Refresh logic: `token-refresh.md`.

## Retrofit (alternative)

Retrofit (`@RestApi`) generates the datasource from an abstract class. It is an option, not the default: a project that already uses Dio directly should keep one style. If adopted, keep the same rules for enums, errors and the 401 interceptor.
