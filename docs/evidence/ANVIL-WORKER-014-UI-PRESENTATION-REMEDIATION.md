# WORKER-014 UI presentation remediation

## Observed trigger

CGPT issued `CGPT_PRODUCT_FINDING: UI_PRESENTATION_INADEQUATE` against the
functionally GREEN Email Builder Campaign Editor. The finding establishes an
ANVIL capability gap: endpoint and test correctness did not by itself meet
the expected standard for a non-technical business tool.

## Bounded response

This branch adds `skills/frontend-product-ui/SKILL.md`, a reusable guidance
document for declaring and checking presentation targets. It is guidance only;
it adds no ANVIL runtime behavior and no application dependency. The North
Star receives only the corresponding product-acceptance clarification.

Email Builder UI changes and their independent audit remain recorded in the
Email Builder WORKER-014 evidence. The skill exists because of that observed
failure, not as speculative framework expansion.

## Acceptance

- Email Builder remediation target: `PRODUCT_USABLE`.
- ANVIL changes: documentation and skill guidance only.
- No provider, routing, scheduler, Redis, broker, or UI runtime machinery was
  added.
