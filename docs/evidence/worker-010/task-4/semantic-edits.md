# Semantic edits

- Added `parse_passed_total` to `anvil/evidence_summary.py` using the accepted
  Qwen call-02 logic, with explicit ASCII ordinal checks, exact slash shape,
  positive denominator, numerator/denominator relationship, and 100000 bounds.
- Added focused valid, malformed, Unicode-digit, boundary, and non-string tests
  in `tests/test_evidence_summary.py`.
- Did not alter `summarize_attempts` or add a summary field. Repository
  inspection found no existing compact `passed/total` field; current evaluator
  evidence uses separate fields, so integration there would be speculative and
  violate the requested existing-path-only condition.
