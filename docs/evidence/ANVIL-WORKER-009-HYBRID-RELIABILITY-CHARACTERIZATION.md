# ANVIL-WORKER-009 — Hybrid Reliability Characterization

## Classification

**HYBRID_RELIABILITY_VIABLE**.

Four materially different bounded ANVIL tasks were run with fresh native
Engineers and the established Qwen3.5 Q4_K_M Ollama path. Qwen produced
mechanically accepted artifacts for 3/4 tasks on the first call and 4/4 within
the permitted two-call bound. All final task audits were GREEN and production
was restored. The sample is small, and Task D required recovery from an
evidence-integrity defect, so this is VIABLE rather than STRONG.

## Campaign contract and runtime

The predeclared contracts are in
[ANVIL-WORKER-009-CAMPAIGN-CONTRACT.md](ANVIL-WORKER-009-CAMPAIGN-CONTRACT.md).
Each task used a fresh native in-session Engineer, no repository context in
the Qwen prompt, `qwen3.5:35b` Q4_K_M, native Ollama `/api/chat`,
`think=false`, temperature `0`, and output cap `384`. Qwen calls were bounded
to two, with call two receiving only exact mechanical failure evidence.

Axiom captured the real production baseline on the host-published port 8010,
stopped only `local-ai-vllm` once for the campaign, and unloaded Qwen before
restoring the original service. The baseline and post-call restoration records
are [production-baseline.json](raw/worker-009/production-baseline.json) and
[production-restoration.json](raw/worker-009/production-restoration.json).
Restoration verified HTTP 200, the expected
`NVFP4/Qwen3-30B-A3B-Instruct-2507-FP4` model and revision, RTX 5090 vLLM
residency, and the unchanged LiteLLM unauthenticated response.

## Task results

### Task A — validation / normalization

Feature: `normalize_model_identifier` in `models.py`, integrated into
`RuntimeConfig.from_environment` to trim and collapse whitespace in externally
supplied model identifiers. Qwen passed on call 1; the exact artifact was
retained with no semantic rewrite. Focused tests passed and the integration
preserved prior configuration behavior. Evidence: [task-a](raw/worker-009/task-a/).

Final audit: **GREEN**, Qwen contract valid, integration valid, high
confidence.

### Task B — parsing / extraction

Feature: `parse_sample_count` in `contracts.py`, integrated as an optional
`sample_count` field in `load_benchmark`, with absent-field behavior preserved.
Qwen passed on call 1; exact artifact retained with no semantic rewrite.
Evidence: [task-b](raw/worker-009/task-b/).

Final audit: **GREEN**, Qwen contract valid, integration valid, high
confidence.

### Task C — calculation / classification

Feature: `classify_success_rate` in `metrics.py`, a deterministic classification
of none/partial/complete acceptance. The existing code had no meaningful
metrics-facing consumer without inventing a new interface, so the Engineer
honestly added the tested reusable utility without forced integration.
Qwen passed on call 1 and was retained exactly. Evidence: [task-c](raw/worker-009/task-c/).

Final audit: **GREEN**, Qwen contract valid, integration/scope decision valid,
high confidence.

### Task D — transformation / rendering

Feature: `escape_markdown_text` in `reporting.py`, integrated into failure-mode
labels in the existing Markdown summary. The first raw Qwen response contained
an unterminated string and did not match a separately saved corrected artifact;
it was correctly reclassified RED and preserved. This was a valid evidence and
artifact-integrity failure, not a model pass. One permitted second call received
the exact compile failure. Its fenced artifact compiled, passed the complete
contract, and was integrated without post-acceptance semantic rewriting.
Evidence, including both calls and reconciliation, is [task-d](raw/worker-009/task-d/).

The stale metadata/test attribution was corrected, and post-call production
restoration was recaptured after the second call. Final audit: **GREEN**, Qwen
contract valid, integration valid, high confidence.

## Campaign metrics

| Metric | Result |
|---|---:|
| Tasks attempted | 4 |
| First-call Qwen pass | 3/4 (75%) |
| Pass within two calls | 4/4 (100%) |
| Complete Qwen failure | 0/4 |
| Extraction/syntax failures | 1 initial raw artifact (Task D), recovered on call 2 |
| Semantic failures | 0 |
| Average Qwen calls/task | 1.25 |
| Accepted artifacts retained without post-acceptance semantic rewrite | 4/4 |
| Final Auditor GREEN | 4/4 |
| Repair rounds | 0; one bounded second-call recovery |
| Final GREEN tasks | 4/4 |

The first-call rate is the direct first-pass measure. The within-two-call rate
includes only the explicitly bounded mechanical-feedback recovery for Task D;
there were no retries beyond that bound and no human intervention.

## Reconciliation and validation

Axiom independently checked each task's file scope, raw evidence, generated
artifact versus integrated source, tests, and unrelated drift. The final tree
passes `PYTHONPATH=. pytest -q` with **87 passed, 66 subtests**, `./ops/validate`,
and `git diff --check`. No production routing or serving configuration changed.

Two Auditors were used sequentially because the collaboration thread limit
prevented four simultaneous fresh Auditors. The first covered A/B and the
second covered C/D; Task D received a fresh post-repair audit after evidence
correction. All final verdicts were GREEN.

## Findings

The pattern is repeatably useful across validation, parsing, classification,
and rendering. Qwen was strongest on small explicit pure functions; the only
failure was a malformed escaping artifact that objective compile/evidence
checks caught, and the bounded second call recovered it. Mechanical checking
was materially useful. The Engineer did not need to semantically rewrite any
accepted Qwen artifact, although Task D's initially saved nonmatching artifact
was correctly rejected.

The campaign demonstrates a 75% first-call and 100% bounded two-call Qwen
success rate across four classes, not broad autonomous coding reliability.
There is no measured need for provider abstraction, routing, Redis, scheduler,
broker, leases, or other orchestration machinery.

## Governance lessons

Useful controls were predeclared contracts, disjoint scopes, fresh Engineers,
bounded calls, exact raw evidence, mechanical evaluation, Axiom-owned
reconciliation, fresh audits, and a hard production restoration gate. The Task
D discrepancy demonstrates why raw response/artifact equality must be checked
before attribution.

Unnecessary controls remain provider interfaces, worker registries, queues,
brokers, leases/fencing, Redis workflow state, and autonomous retry loops. The
one additional evidence-reconciliation action solved an observed problem and
did not justify architecture expansion.
