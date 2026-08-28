# Semantic edit separation

## Qwen code

Stored verbatim as extracted artifacts in `qwen-call-01-artifact.py` and
`qwen-call-02-artifact.py`; neither was integrated because both failed the
contract.

## Engineer integration

`anvil/reporting.py` adds a native `format_failure_rate` using strict integer
validation and `decimal.localcontext()` with `ROUND_HALF_EVEN`. `write_summary`
adds `- Failure rate:` immediately after the existing Pass line. Focused tests
cover zero, partial, complete, half-even rounding, invalid inputs, ordering,
and existing Markdown escaping.
