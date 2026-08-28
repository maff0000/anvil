# Integration notes

## Delegation result

Decision: `NATIVE_PLUS_QWEN`.

Qwen supplied the isolated `classify_success_rate(accepted, samples)` logic in
`qwen-call-01-artifact.py`. The existing `anvil/metrics.py` implementation
matches that artifact exactly in validation branches, return values, and
deterministic behavior; it was retained without repair or semantic alteration.

Call 1 passed its declared mechanical contract. The later call-2 response was
not needed, was not justified by a mechanical failure, and contributed nothing
to acceptance. The task's actual Qwen result is therefore first-call GREEN.

## Engineer-owned integration

The Engineer integration imports `classify_success_rate` into
`anvil/evidence_summary.py` and adds `classify_success_rate` to the returned
summary after `accepted` is computed. Existing keys, counting semantics,
validation, and aggregate calculations are unchanged. Focused tests assert
`none`, `partial`, and `complete` summary outcomes.
