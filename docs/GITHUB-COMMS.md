# GitHub communications

Issue #1, `ANVIL BETA CONTROL — Axiom ↔ CGPT`, is the control channel.

Axiom messages are `AXIOM_HEARTBEAT`, `AXIOM_QUERY`, `AXIOM_CHECKPOINT`,
`AXIOM_BLOCKED`, and `AXIOM_DELIVERY_CANDIDATE`. CGPT responses are
`CGPT_ACK`, `CGPT_RULING`, `CGPT_FINDING`, `CGPT_ACCEPT`, and `CGPT_REJECT`.

Messages include UTC, SHA, phase, evidence, and query/blocker state as
applicable. Heartbeats are compact liveness records, not progress claims, and
are approximately 15 minutes only during active delivery work. Per-inference
activity is never posted.
