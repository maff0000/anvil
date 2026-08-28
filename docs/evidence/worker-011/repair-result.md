# ANVIL-WORKER-011 acceptance repair

Finding: the implementation was valid, but final delivery evidence was absent
and integration coverage was not explicit.

Action: added one raw ANVIL-result-shape integration test covering
`build_result_manifest` aggregation and deterministic `write_result_manifest`
output. No product implementation was changed.

Tests: focused manifest pytest, full pytest, `./ops/validate`, and
`git diff --check` all passed; human intervention remained 0.
