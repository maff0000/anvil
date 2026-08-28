# ANVIL — North Star Architecture

## Purpose

ANVIL is a lightweight development-control system for taking software
projects from Human/CGPT-defined product intent to independently scrutinised
delivery.

Its purpose is to let a Human point ANVIL at a new, existing, incomplete, or
partially broken project while Axiom establishes repository truth, holds the
PID as authority, decomposes and sequences work, chooses suitable Engineer
paths, uses bounded coding capabilities where useful, reconciles changes,
runs tests, obtains independent Auditor scrutiny, routes valid repairs, and
maintains clean Git/GitHub history before returning a delivery candidate.

The destination is:

```text
Human + CGPT
     ↓
    PID
     ↓
   Axiom
     ↓
Engineers / bounded coding capabilities
     ↓
reconciliation + tests
     ↓
independent Auditor
     ↓
bounded repair when required
     ↓
GitHub delivery candidate
     ↓
Human + CGPT final scrutiny
```

Human involvement belongs at product authority and final acceptance, not at
routine implementation or repair decisions.

## Core doctrine

**Capability first. Architecture second.**

ANVIL is built only around empirically proven capabilities. Every mechanism
must solve an observed problem. Existing platform capabilities and standard
tools are preferred over custom machinery.

For user-facing work, technical correctness alone does not imply product
acceptance. Human/CGPT may issue a `PRODUCT RED` finding against a technically
GREEN implementation, returning it to the bounded repair loop. User-facing
PIDs should declare a presentation target where relevant, such as
`FUNCTIONAL_ONLY`, `PRODUCT_USABLE`, or `PRESENTATION_POLISHED`.

Already demonstrated capabilities include native Engineer and Auditor
subagents, standard Git clone isolation, GitHub delivery, bounded local-Qwen
coding, and ordinary Python virtual environments. ANVIL must not hide weak
models or unreliable workers behind orchestration complexity.

## Authority model

### Human + CGPT

Own product intent, PID definition, major product/architectural authority,
and final independent scrutiny.

### Axiom

Axiom is the Project Lead. It owns repository discovery, decomposition,
sequencing, execution-path choice, Engineer/Auditor invocation,
reconciliation, testing, Git, PR lifecycle, and acceptance or rejection inside
the autonomous loop.

### Engineer

The Engineer owns bounded implementation within the authorised scope. It does
not own product authority, Git lifecycle, or final acceptance.

### Auditor

The Auditor independently challenges implementation against the PID and
repository truth. It does not edit during audit. A RED finding is evidence for
Axiom to adjudicate and route to a fresh repair Engineer.

## Durable truth

ANVIL must be reconstructable from repository contents, PID, constraints,
committed evidence, and Git history. Git is durable code, history, and
evidence truth. GitHub is durable external collaboration and scrutiny truth.
Transient runtime state is not architectural truth. Redis or another live
state mechanism may be introduced only if an observed operational problem
genuinely requires it.

## Project integration model

ANVIL runtime code is not copied into governed applications, and applications
do not import or depend on ANVIL. A governed project may eventually carry a
small self-describing control envelope such as:

```text
project/
├── .anvil/
│   ├── project.yaml
│   ├── CURRENT-TRUTH.md
│   └── constraints.md
├── docs/
│   ├── PID-...
│   └── evidence/
├── application code
└── tests
```

The exact `.anvil/` contract is not frozen. It will be introduced
incrementally only when real projects prove which information is necessary.

## Central ANVIL

ANVIL remains a separate project/runtime responsible for Axiom,
Engineer/Auditor capability, bounded local-GPU capability, execution
doctrine, clean workspace strategy, and Git/GitHub delivery. Multiple
projects must be able to proceed independently without contaminating one
another.

```text
                    ANVIL
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
       Project A   Project B   Project C
        .anvil/     .anvil/     .anvil/
```

## Workspace doctrine

The developer working directory is not necessarily the delivery workspace.
The preferred flow is:

```text
authoritative GitHub baseline
         ↓
fresh isolated clone
         ↓
dedicated feature branch
         ↓
Axiom / Engineers / Auditor
         ↓
tests and evidence
         ↓
GitHub PR
```

This protects dirty worktrees, parallel projects, Git provenance, and
reproducibility. WORKER-013 demonstrated that standard clean-clone isolation
is sufficient for an external project and needs no custom workspace
framework.

## Local GPU doctrine

Local GPU inference is a bounded coding capability, not the system architect
or an autonomous repository worker:

```text
Axiom / native Engineer
        ↓
isolated deterministic subtask
        ↓
bounded Qwen call
        ↓
mechanical evaluation
        ↓
accepted artifact or exact RED feedback
```

Use Qwen for isolated, low-context, mechanically testable work likely to save
Engineer effort. Do not use it merely because GPU capacity exists.
`GREEN_ARTIFACT_HARD_STOP` is mandatory.

## Anti-bloat doctrine

Do not introduce without observed need:

- broker infrastructure or a generic worker runtime;
- nested sandboxing, project registries, or provider abstractions;
- workflow DSLs, Redis orchestration, schedulers, or lease machinery;
- autonomous daemons or a generic ANVIL SDK copied into projects.

Standard operating-system, Git, Python, container, and GitHub primitives are
preferred.

## Half-built project workflow

Recovering and continuing partially built projects is a primary use case:

```text
point ANVIL at repository
       ↓
DISCOVER
       ↓
establish CURRENT-TRUTH
       ↓
identify working / broken / unfinished state
       ↓
Human + CGPT decide next useful outcome
       ↓
PID
       ↓
autonomous Axiom delivery loop
```

ANVIL must not assume old documentation or local worktrees are correct;
repository and runtime evidence establish truth.

## Multi-project goal

Each independent project should have its own authoritative repository, PID,
isolated delivery workspace, Axiom loop, Git branch/PR, and evidence trail.
No project should require ANVIL application code to be embedded in it.

## Proven state

The empirical chain demonstrates native Engineer and Auditor viability,
bounded RED-to-repair-to-GREEN, dependent work-item delivery, verified local
Qwen coding, Axiom execution-path judgment, external Git authority through
clean clones, baseline provenance handling, and cross-project Email Builder
delivery with zero Human intervention inside the implementation loop.

WORKER-013 demonstrated `CROSS_PROJECT_PORTABILITY_VIABLE` without Email
Builder importing ANVIL or requiring new ANVIL framework machinery.

## Current direction

Do not build the final framework from speculation. Progress bit by bit through
useful projects. Each real project should expose the next missing capability;
generalise only the smallest mechanism that a repeated need justifies. Keep
one-off behavior project-specific when no repeated need exists.

The immediate proving ground is Email Builder, with the next product direction
being a genuinely usable Campaign Editor while continuing to validate ANVIL's
delivery model.

## North-star success condition

ANVIL succeeds when a Human can say:

> Here is what I want this product to become.

ANVIL then discovers the state, executes the development loop, independently
scrutinises delivery, preserves clean Git/GitHub truth, and returns a
trustworthy delivery candidate while the Human remains outside routine
implementation and repair work.
