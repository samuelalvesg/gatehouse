---
name: infra-config-review
description: Review of infrastructure and delivery configuration (Dockerfiles, Compose, Kubernetes manifests, Terraform, CI pipelines, environment files) for privilege, secrets, pinning and exposure. Use when a change touches build, deploy, container or infrastructure files.
---

# Infrastructure configuration review

Read the files that define how the software is built, shipped and run. A mistake here reaches production without touching the application code.

## Checklist

- **I1 Non-root.** Containers run as a non-root user. No `USER root` left in the final stage.
- **I2 Pinned images.** Base images use a fixed version or digest, not `latest`.
- **I3 Secrets in build.** No secret is passed as a build argument, copied into a layer, or printed in a build log. Use the build system's secret mechanism.
- **I4 Minimal image.** The final stage has only the runtime and the application. No compilers, package managers or shells that the app does not need.
- **I5 Exposed ports and hosts.** Only the required ports are published. Admin, debug and metrics endpoints are not on a public interface.
- **I6 Privileges.** No privileged container, host networking, host path mounts or added capabilities without a written reason. Kubernetes: no `runAsUser: 0`, no `allowPrivilegeEscalation: true`, resource limits set.
- **I7 Health probes.** Liveness and readiness probes are defined and do not call expensive endpoints (see `release-safety-review`, R7).
- **I8 Pipeline secrets.** Pipelines read secrets from the platform store. Logs do not echo them. Third-party actions and steps are pinned to a version or commit.
- **I9 Pipeline permissions.** The pipeline token has the minimum permissions. Pull-request workflows from forks do not receive secrets.
- **I10 Infrastructure as code.** Public storage, open security groups (`0.0.0.0/0` on administrative ports), unencrypted volumes and disabled logging are flagged. Each exception is named in the file.
- **I11 Environment files.** Real values are not committed. Development and production values are separate, and the `.env` pattern is ignored by git.
- **I12 Drift.** The deployed state comes from the files. A manual change is recorded or reverted.

## Procedure

1. List the infrastructure and pipeline files changed by the diff: `Dockerfile*`, `compose*.yml`, `*.tf`, `k8s/`, `.github/workflows/`, `.gitlab-ci.yml`, `*.env*`.
2. For each file, run the checklist. Mark items that do not apply as `N/A`.
3. Where a tool is available (`hadolint`, `trivy config`, `checkov`, `kube-linter`), run it and cite its output. If it is not installed, mark the dependent items `NOT VERIFIED` and say which tool is missing.

## Output

One table, the same format as `web-app-security-audit`: ID, check, status (`PASS`, `FAIL`, `N/A`, `NOT VERIFIED`), severity, evidence (`file:line`), fix.

## Related skills

Application-level checks: `web-app-security-audit`. Rollout and rollback: `release-safety-review`. Threat model of the deployed system: `threat-modeling`.
