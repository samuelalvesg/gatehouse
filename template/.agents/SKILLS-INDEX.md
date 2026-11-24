# Skills by signal

Read this file to choose the narrowest skill for a task. Load one to three skills per pass; add another only when its signal is present.

| Signal in the task | Skills to load | Add when |
|---|---|---|
| Web app, API routes, auth, uploads, client bundle | `web-app-security-audit` | a login or hashing path is involved: also check its G4–G9 items |
| Login, passwords, sessions, client IP | `web-app-security-audit` | a shared proxy or edge sits in front: check G8 |
| Threat model, new trust boundary, new privileged role | `threat-modeling` | a new third-party data flow |
| Writes from several steps, retries, webhooks, money, quotas, cache | `data-consistency-review` | the change touches a cache (C12–C13) |
| Public or cross-team API, event or webhook schema changes | `api-change-review` | the change also touches the release (`release-safety-review`) |
| Migration, feature flag, rollout, rollback, backup | `release-safety-review` | the release changes data (R1–R3) |
| Dockerfile, Compose, Kubernetes, Terraform, CI pipeline | `infra-config-review` | a secret is passed to the build |
| Any test that sends traffic to a running system | `authorized-testing` | always, with `scripts/security/scope_check.py` first |
| Backlog item creation, status change, done report | `backlog-items`, `backlog-check` | a triage question: `backlog-triage` |
| Tests, flaky behaviour, coverage | `test-strategy`, `test-mutation-audit` | |
| Bug with unknown cause | `root-cause-debug` | |
| Architecture decision | `adr-writer` | |

Before publishing or merging a change to agent instructions, run `python3 scripts/security/scan_skill_injection.py`. Every line it reports needs a reading, not an automatic removal.
