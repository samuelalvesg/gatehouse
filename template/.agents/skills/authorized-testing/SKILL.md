---
name: authorized-testing
description: Rules for any active test of a system (validating a finding, probing a staging app, checking a control under load): written scope, authorization, safe fixtures, a verifier before a finding is reported, and the report format. Use before running any test that sends traffic to a running system.
---

# Authorized testing

Testing a running system is allowed only with written authorization for that exact target and window. Without it, stop at the source-code review (see `web-app-security-audit`).

## Before any test

1. **Scope file.** The owner writes a scope file (owner, who authorized, environment, valid dates, allowed hosts). Check it with `python3 scripts/security/scope_check.py <scope.json> <target>`. Exit 0 is required; anything else stops the work.
2. **Environment.** Staging, or a copy created for the test. Never production, unless the scope file says so in writing.
3. **Fixtures.** Dummy accounts, dummy data, dummy payment methods. No real users, no other tenants' data.
4. **Limits.** Load and availability tests run only on a dedicated environment. Do not test availability on a shared service.

## During a test

- Stay inside the scope file. A new host or path that appears in a response is out of scope until the owner adds it.
- Stop and report when the test starts to affect other users, when data is changed that the fixture did not create, or when a response shows real personal data.
- Record every request that changed state, so it can be reverted or explained.

## Verification gate

A finding is reported as `CONFIRMED` only when a second pass reproduces it from the written steps and the evidence is attached. A reviewer who did not run the test reads the steps and the evidence, and tries to disprove the finding. A finding that cannot be reproduced is `NOT VERIFIED`, with the reason. Never report a suspicion as a confirmed issue.

## Report

Each finding:

| Field | Content |
|---|---|
| ID | Check ID from `web-app-security-audit`, plus the OWASP WSTG test ID (v4.2) when one applies |
| Status | `CONFIRMED`, `NOT VERIFIED` or `REJECTED` (disproved by the verifier) |
| Severity | `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, with the reason |
| Scope | Host, path, environment, date of the test |
| Steps | Exact steps, with dummy data, so anyone can repeat them |
| Evidence | Response excerpt or screenshot, with personal data removed |
| Fix | The change that closes it, and how to verify the fix |

## Related skills

Checklist and source review: `web-app-security-audit`. Data consistency under concurrency: `data-consistency-review`. Evidence format: `evidence-report`.
