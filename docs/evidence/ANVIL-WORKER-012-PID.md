# PID — ANVIL-WORKER-012-REPRESENTATIVE-PID-SLICE

## Product intent

Build a coherent Benchmark Run Bundle capability. A completed benchmark run
must produce durable, deterministic artifacts from one validated source record
set: a result manifest, a human-readable Markdown summary, and a machine-
readable bundle index. ANVIL must safely write the bundle and verify it on
read-back.

## User-visible outcome

Given valid completed benchmark records and a target directory, ANVIL produces
one inspectable bundle containing:

- `manifest.json` with aggregate result fields;
- `summary.md` with deterministic human-readable results;
- `index.json` describing the bundle schema and exact artifact names.

The bundle can be verified against the original records. Invalid input or a
failed write does not present a misleading completed bundle.

## Acceptance criteria

1. One source record set drives every generated artifact.
2. Manifest and Markdown summary are deterministic.
3. Bundle index has stable schema/version fields and exact artifact references.
4. Malformed or inconsistent records are rejected before misleading output is
   committed.
5. Existing valid bundle output is preserved when a later validation fails.
6. Read-back verification catches missing, malformed, or inconsistent artifacts.
7. Implementation is standard-library only and does not change model/provider/
   runtime architecture.
8. Focused, integration, full ANVIL, validation, diff, and fresh Auditor checks
   are GREEN.

## Invariants

- Manifest, summary, and index describe the same records and counts.
- Artifact names and schema/version values are stable.
- Verification never mutates the bundle.
- A failed bundle attempt cannot be accepted as complete.
- Git remains Axiom-owned.

## Non-goals

No generic artifact framework, database, broker, scheduler, provider layer,
Redis workflow state, daemon, model routing, or production service change.

## Dependent work items

WI-1 builds/refines the deterministic summary representation.
WI-2 depends on WI-1 and existing manifest capability to build the bundle index.
WI-3 depends on WI-1 and WI-2 to safely write all artifacts as a coherent
bundle. WI-4 depends on the completed bundle writer and verifies the bundle
against source records. Integration tests depend on all four.

## Completion definition

The PID is complete only when an actual representative bundle is generated,
read-back verification passes, deliberate artifact corruption is rejected,
invalid input preserves a prior valid bundle, all tests/validation pass, a
fresh independent Auditor returns GREEN, evidence is pushed to GitHub, and
`DELIVERY_STATUS: DELIVERY_CANDIDATE` is recorded with zero Human intervention
inside the implementation/audit loop.
