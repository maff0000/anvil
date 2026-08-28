# ANVIL-WORKER-010 — Delegation Decision Quality

## Classification

**DELEGATION_DECISION_VIABLE**.

Axiom made six explicit manual execution-path decisions. All six final
features are GREEN and all six final Auditor implementation verdicts are
GREEN. The native-only choices were consistently efficient; bounded Qwen was
useful for two of three selected Qwen tasks, but one selection produced no
implementation benefit. This is a viable manual judgment pattern, not a case
for automated routing or a STRONG classification.

## Campaign contract and decisions

The predeclared work items are in
[ANVIL-WORKER-010-CAMPAIGN-CONTRACT.md](ANVIL-WORKER-010-CAMPAIGN-CONTRACT.md),
and decisions were committed before implementation in
[ANVIL-WORKER-010-DECISIONS.md](ANVIL-WORKER-010-DECISIONS.md). Each task used
a fresh native Engineer; Qwen, where selected, received only a bounded
function contract. Axiom retained reconciliation and Git authority.

| Work item | Useful feature | Chosen path | Decision assessment | Result |
|---|---|---|---|---|
| 1 | Validate positive runtime settings | NATIVE_ONLY | GOOD | GREEN |
| 2 | Wire optional benchmark `sample_count` | NATIVE_ONLY | GOOD | GREEN after repair |
| 3 | Expose success classification in summaries | NATIVE_PLUS_QWEN | GOOD | GREEN; Qwen retained |
| 4 | Strict ASCII `passed/total` parser | NATIVE_PLUS_QWEN | GOOD | GREEN; call 2 recovered call 1 |
| 5 | Harden JSONL evidence writing | NATIVE_ONLY | GOOD | GREEN |
| 6 | Add Markdown failure-rate rendering | NATIVE_PLUS_QWEN | POOR in retrospect | GREEN natively; Qwen failed |

## Per-item results

### Work item 1 — native-only runtime validation

The Engineer added positive-integer validation at the configuration boundary,
including malformed, boolean, zero, and negative inputs. This was direct
repository-context work with no Qwen calls. Focused tests and validation passed.
The Auditor returned GREEN and judged NATIVE_ONLY GOOD.

### Work item 2 — native-only runner integration

The Engineer wired optional `Benchmark.sample_count` into `run()` while
preserving explicit caller counts and legacy configuration fallback. The first
implementation missed `ops/run-benchmark`, which an Auditor detected. A fresh
native repair corrected that path. No Qwen was used. Final focused/full tests,
validation, scope, and audit passed. The native-only decision remained GOOD
because the defect was a normal repository-integration issue, not evidence
that Qwen would have reduced the work.

### Work item 3 — Qwen-assisted summary classification

Qwen supplied `classify_success_rate(accepted, samples)` and the exact logic
was retained. The Engineer integrated it into `summarize_attempts` without
semantic rewrite. The first artifact passed; a second call was made only
because an integration/test-discovery check exposed a problem, and produced
equivalent logic. Final Auditor: GREEN; delegation choice GOOD.

### Work item 4 — Qwen-assisted strict parser

Qwen call 1 used `str.isdigit()` and failed the ASCII-only requirement because
Unicode digits were accepted. Exact mechanical failure was supplied to call 2;
the corrected artifact passed and was retained. The Engineer added the parser
without forcing an integration seam that did not exist. Final Auditor: GREEN;
delegation choice GOOD.

### Work item 5 — native-only evidence hardening

The Engineer made `write_jsonl` validate all records before filesystem changes
and create missing parent directories, preserving valid output behavior. This
was I/O sequencing and test-hardening work where Qwen would have added
ceremony. Final Auditor: GREEN; delegation choice GOOD.

### Work item 6 — Qwen-selected mixed rendering task

Qwen was given a bounded `format_failure_rate(failures, samples)` contract.
Both permitted calls failed: call 1 had an inverted type guard; call 2 fixed
that but mutated global decimal context and returned fenced output. Neither
artifact was integrated. The Engineer implemented an independent local-context
helper and report line; this final feature is GREEN but is not a hybrid Qwen
success. Qwen reduced no Engineer effort. Final Auditor: GREEN for the native
implementation and evidence; Axiom records the path as POOR in retrospect and
counts one path-switch regret.

## Metrics

| Metric | Result |
|---|---:|
| Work items | 6 |
| Native-only | 3 |
| Native-plus-Qwen | 3 |
| Qwen-selected first-call pass | 1/3 (33.3%) |
| Qwen-selected pass within two calls | 2/3 (66.7%) |
| Complete Qwen failure | 1/3 (33.3%) |
| Accepted Qwen artifacts requiring semantic rewrite | 0 |
| Final Auditor GREEN | 6/6 |
| Final GREEN features | 6/6 |
| Fresh Engineer invocations | 7 (six initial, one Task 2 repair) |
| Qwen calls | 6 |
| Repair rounds | 1 native Task 2 repair |
| Auditor choices judged GOOD | 5 |
| Auditor choices judged ACCEPTABLE | 0 |
| Auditor choices judged POOR | 1 |
| Path-switch regret | 1 (Task 6) |

No call exceeded the two-call limit and no automatic router was used.

## Counterfactual review

Qwen was used selectively rather than reflexively. Tasks 3 and 4 were good
bounded-generation choices: their contracts were isolated, mechanical, and
Qwen materially supplied accepted logic. Task 6 had the right surface shape
but observed model behavior made native-only materially better; it is the
single regret in this six-item sample. Tasks 1, 2, and 5 were correctly kept
native-only because configuration, cross-file compatibility, and I/O safety
dominated their effort.

Mechanical checks caught both Qwen contract failures and the Task 2 integration
omission. The evidence does not justify automated routing.

## Production and validation

Qwen tasks ran in one controlled exclusive GPU window. Qwen GPU evidence was
captured in each selected task directory. Qwen was unloaded and the original
production vLLM was restored without configuration or routing changes. The
published port 8010 returned health 200, the expected model/revision was
present, RTX 5090 residency was restored, and LiteLLM remained reachable with
its normal unauthenticated response.

Final validation: `PYTHONPATH=. pytest -q` — **121 passed, 94 subtests**;
`./ops/validate` — **57 tests passed**; `git diff --check` — GREEN. The
worktree was reconciled for exact task scope and no unrelated source drift.

## Governance lessons

Useful governance was limited to predeclared contracts, explicit manual path
decisions, fresh Engineers, bounded Qwen calls, mechanical acceptance, raw
evidence, Axiom reconciliation, fresh independent audits, and production
restoration. No routing layer, scorecard, policy DSL, registry, Redis state,
broker, scheduler, lease, or unattended mechanism was justified.

The evidence supports manual delegation judgment as viable. It does not
support encoding that judgment into an automated router; the next boundary
should be chosen only after CGPT scrutiny of this small mixed sample.

## Corrective governance rule

`GREEN_ARTIFACT_HARD_STOP`: once a bounded Qwen artifact passes its declared
mechanical contract, no further model call is permitted for that subtask unless
a new independently authorized subtask exists. WORKER-010 Task 3 call 2 was
unnecessary and procedurally non-compliant; it is not treated as evidence of
additional capability.
