# ANVIL-WORKER-012 — Representative PID Slice

## Delivery declaration

`DELIVERY_STATUS: DELIVERY_CANDIDATE`
`HUMAN_INTERVENTION_DURING_LOOP: 0`
`CLASSIFICATION: REPRESENTATIVE_SLICE_VIABLE`

## PID and decomposition

The PID required a useful Benchmark Run Bundle driven by one validated source
record set. The dependent sequence was:

`WI-1 summary → WI-2 index → WI-3 atomic writer → WI-4 read-back verifier`

All four work items were real, bounded, and selected `NATIVE_ONLY`. Qwen was
not used: each item depended on existing ANVIL interfaces, cross-artifact
consistency, filesystem atomicity, or repository integration. No production
service, model, provider, or runtime configuration changed.

## Engineer execution and reconciliation

- WI-1 added deterministic `build_bundle_summary`, reusing the established
  normalization and Markdown report semantics.
- WI-2 added deterministic `build_bundle_index` with stable schema/version and
  exact `manifest.json`, `summary.md`, and `index.json` references.
- WI-3 added `write_run_bundle`, building/serializing all artifacts before a
  temporary sibling-directory swap and rollback; invalid input preserves an
  existing valid bundle.
- WI-4 added read-only `verify_run_bundle`, requiring exact artifact equality
  with deterministic outputs for the supplied records.

Axiom independently checked each actual diff, scope, dependency, tests, and
Git state. No substantive PL coding takeover occurred. There were four fresh
Engineer invocations, no repair Engineer, and no Qwen calls.

## Integration proof

The focused integration checks produced 15 passed tests covering valid
write/read-back, each missing artifact, malformed JSON, altered manifest and
index values, altered summary, and invalid source records. The existing-valid-
bundle preservation case passed. Unrelated files are ignored by verification.

Full validation:

- `PYTHONPATH=. pytest -q`: 159 passed, 94 subtests passed.
- `./ops/validate`: 57 tests passed.
- `git diff --check`: clean.
- Production vLLM health on published port 8010: HTTP 200; expected model
  remained reported. No GPU window was required because Qwen was not selected.

## Audit and adjudication

The first fresh Auditor returned RED only for missing delivery-status evidence
and missing explicit GitHub-push evidence; it found no implementation defect.
Axiom adjudicated this as a valid evidence-completion finding, added this
durable declaration/report, committed it, and pushed it. A fresh re-audit is
the final acceptance gate for this candidate.

## Git and governance

Worker commits are `14abc1b` (PID), `ffaeae0` (plan), `5aaf9c4` (summary),
`b5a3afc` (index), `3ca330e` (writer/verifier), and `12eb7fe`
(integration proof). The feature branch is pushed for the delivery PR.

Useful controls were the PID, explicit dependency order, fresh Engineer and
Auditor separation, independent reconciliation, deterministic tests, bounded
evidence, and Axiom-owned Git. Unnecessary controls were Qwen delegation,
Redis, leases, brokers, schedulers, provider abstractions, and runtime
interruption. The slice exposed no new governance mechanism requirement.

`DELIVERY_STATUS: DELIVERY_CANDIDATE`
