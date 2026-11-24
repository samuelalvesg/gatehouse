---
name: local-llama-bridge
description: Delegates mechanical, verifiable tasks to local models (Ollama on localhost:11434), with local×cloud routing, fixed parameters and deterministic verification. Use BEFORE bulk boilerplate generation, test stubs or summarizing large logs.
---
**Execution:** LOCAL ONLY (`localhost:11434` does not exist in the cloud). In the cloud this skill does not apply: the cloud model does the task.

# When to delegate (cloud agent decides)
Delegate only if **all 3** hold:
1. **Repetitive/voluminous** work (heuristic, **not measured**: ≥ ~10 similar units, or log > ~300 lines). Few units: do it directly; writing the prompt and checking costs more.
2. A **deterministic verifier** exists on the other side (compiler, test, schema, `grep -F`, migration checker).
3. The user **authorized** Ollama for this task (ask first; project MCP for Ollama only on request). No authorization → do not call.

# Local × cloud matrix
| Task | Where | Verifier (wins on disagreement) |
|---|---|---|
| DTO/entity/schema from an **existing example** | local (`llama-boilerplate-dev`) | build, module tests |
| Format conversion (C#→Dart, JSON→proto) | **generator first** (`protoc`, `build_runner`, ORM tooling). Local only if no generator | compile + round-trip test |
| Simple CRUD controller | local | build + integration tests |
| Test stub (structure + mocks) | local (`llama-test-stubber`) | compiles and **is red** |
| Compact log/stack trace | deterministic script first; local optional (`llama-log-summarizer`) | every quoted line exists in the original |
| Migration | **no**: the ORM generator + migration checker | — |
| **Open-ended** issue/bug triage/classification | **no** (measured: 61% agreement between 14b and 7b; reviewer approved 3/3 wrong). Deterministic rule only (path, keyword) | rule |
| Architecture, spec, cross-impact, security, performance, multi-module refactor, pricing/legal | **always cloud** | — |

# Hard rules
- **Local output is a PROPOSAL.** The model **never edits repo files**. The cloud agent writes after the verifier passes. Verifier and model disagree → the verifier wins.
- Input = **one** model file from the repo (few-shot) + the task. The cloud agent already ran `graph-mapping` and chose the base model file; the local model does not explore the repo.
- No secret/PII in the prompt (logs pass through deterministic redaction first: tokens, keys, e-mails).
- **Separate** passes: generate ≠ review. Never "generate and fix" in one call.
- Rejected batch: **split in half** and repeat (with `temperature 0` + fixed `seed`, repeating verbatim reproduces the failure).
- 3 consecutive timeouts → abort, save the partial, return to the cloud agent.
- Local output goes to a disposable scratch dir, never straight into the tree.
- Final report with `evidence-report`: model, parameters, how many units passed/failed the verifier, what the cloud redid.

# Parameters (HTTP, not `ollama run`)
`temperature: 0`, fixed `seed`, **explicit `num_ctx`** (the default silently truncates), bounded `num_predict`, `stream: false`. Structured output: `format: "json"` (or JSON Schema if the Ollama version supports it: check `ollama --version`). Which model is best per task: **not measured**; run a small battery with the verifier before fixing one.

# Call
```bash
curl -s localhost:11434/api/tags | jq -r '.models[].name'            # what exists
curl -s localhost:11434/api/generate -d @- <<'JSON' | jq -r .response
{"model":"<model>","system":"<profile system prompt>","prompt":"<task + example>",
 "stream":false,"options":{"temperature":0,"seed":42,"num_ctx":8192,"num_predict":2048}}
JSON
```
```python
# stdlib; split in half on rejection
import json, urllib.request
def ask(model, system, prompt, num_ctx=8192, timeout=120):
    body = {"model": model, "system": system, "prompt": prompt, "stream": False,
            "options": {"temperature": 0, "seed": 42, "num_ctx": num_ctx, "num_predict": 2048}}
    req = urllib.request.Request("http://localhost:11434/api/generate",
                                 json.dumps(body).encode(), {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)["response"]
def run_batch(items, verify, model, system):   # verify(item, out) -> bool (deterministic)
    ok, bad = [], []
    for it in items:
        out = ask(model, system, it)
        (ok if verify(it, out) else bad).append((it, out))
    return ok, bad   # bad: resend split in half; 3 consecutive failures: stop
```
For large volume use a **standalone script** (log to file, timeout, abort after 3, save partial), not call-by-call from the session.

# Profiles (`.agents/agents/local/`)
`llama-boilerplate-dev` · `llama-test-stubber` · `llama-log-summarizer`. They are **prompt/parameter profiles**, not Claude subagents.

# Checklist
- [ ] 3 delegation conditions met (volume, verifier, authorization)
- [ ] existing deterministic generator ruled out first
- [ ] base model file chosen by the cloud
- [ ] fixed parameters; explicit `num_ctx`
- [ ] verifier ran; failures reported
- [ ] nothing written by the model; cloud applied it
