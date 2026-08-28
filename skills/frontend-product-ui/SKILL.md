# Frontend product UI guidance

This is lightweight delivery guidance for user-facing web work. It is not
ANVIL runtime code, and governed applications must not import ANVIL because
of it.

## Establish the target

Classify the PID's presentation target explicitly:

- `FUNCTIONAL_ONLY`: behavior and basic operability are the target.
- `PRODUCT_USABLE`: a coherent business-facing interface is required.
- `PRESENTATION_POLISHED`: visual refinement beyond ordinary product usability
  is part of acceptance.

When a PID calls for a usable user-facing business tool, default to at least
`PRODUCT_USABLE`. Technical tests alone do not establish that target.

## Engineer workflow

1. Inspect the existing application's templates, CSS, components, and UI
   conventions before introducing styling or changing structure.
2. Preserve the existing behavior, security boundaries, and rendering path.
3. Establish a clear visual hierarchy with readable typography, intentional
   spacing, grouped related controls, useful field sizing, and an obvious
   primary action.
4. Design error, empty, loading, and preview/output states as part of the
   feature. Use semantic structure, labels, keyboard-focus visibility, and a
   sensible responsive fallback.
5. Prefer the application's existing framework and local/native CSS. Avoid
   frontend stacks, build pipelines, and external CDN/runtime dependencies
   unless the PID explicitly justifies them.
6. Inspect the rendered/user-facing result in addition to source inspection
   and route tests. Record what was actually checked.

Avoid raw browser-default presentation for a product-facing feature unless
that is explicitly authorized by the PID. Keep the smallest local change that
reaches the declared presentation target.

## Auditor checklist

Auditors challenge actual usability, not only endpoint correctness. Check the
declared target, hierarchy, spacing, typography, grouping, responsive layout,
action distinction, validation/error treatment, accessibility basics,
preview/output framing, and behavior/security regressions. Require evidence
from the rendered or application-level user flow where practical.

If the implementation is technically GREEN but misses a declared user-facing
presentation target, report `PRODUCT RED` with concrete evidence. Axiom
adjudicates the finding and routes any repair through the normal bounded loop.
