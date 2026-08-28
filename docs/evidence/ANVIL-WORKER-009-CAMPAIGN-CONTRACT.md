# ANVIL-WORKER-009 campaign contract

This contract was committed before any trial. The four trials are independent
and use fresh native Engineers, the same Qwen runtime/settings, and mechanical
acceptance. They are run sequentially inside one controlled GPU window where
safe; Axiom owns opening and closing that window.

## Common rules

Qwen receives only the task-specific function contract below. It may not see
repository context, choose files, use tools, or edit the repository. Each
trial permits at most two calls: call two only after exact mechanical failure
evidence from call one. No third call. Generated code is extracted, compiled,
and tested independently before integration.

Runtime: `qwen3.5:35b`, Q4_K_M, native Ollama `/api/chat`, `think=false`,
temperature `0`, output cap `384`. GPU backing must be proven with `/api/ps`
and container NVIDIA evidence. Raw requests/responses and evaluations belong
under `docs/evidence/raw/worker-009/task-{a,b,c,d}/`.

## Task A — validation / normalization

Useful feature: normalize externally supplied model identifiers before runtime
configuration uses them.

Engineer scope: `anvil/models.py`, `tests/test_models.py`, and task-A raw
evidence. Integrate the accepted helper in `RuntimeConfig.from_environment`
for `ANVIL_MODEL`; preserve all other configuration behavior.

Qwen subtask:

```python
normalize_model_identifier(value: str) -> str
```

The input must be a `str` and not `bool`; otherwise raise `ValueError`. Strip
surrounding whitespace, collapse every run of internal whitespace to one
ASCII space, and return the result. An empty normalized value raises
`ValueError`. Do not alter non-whitespace characters, including `/`, `:`, `-`,
`.`, and Unicode. Standard library only; no filesystem/network/global state.
Examples: `"  qwen3.5:35b  " -> "qwen3.5:35b"`,
`"NVFP4 / Qwen  30B" -> "NVFP4 / Qwen 30B"`.

Acceptance: helper contract tests, RuntimeConfig environment integration tests,
full ANVIL tests and validation.

## Task B — parsing / extraction

Useful feature: parse a compact benchmark result count used by report/evidence
inputs.

Engineer scope: `anvil/contracts.py`, `tests/test_contracts.py`, and task-B
raw evidence. Integrate the helper into `load_benchmark` only for an optional
`sample_count` field, preserving existing behavior when absent.

Qwen subtask:

```python
parse_sample_count(value: str) -> int
```

Accept only a non-empty string consisting of ASCII decimal digits with no
leading `+`/`-`, surrounding whitespace, decimal point, or other characters.
Return its base-10 integer value. It must be at least 1 and at most 100000;
otherwise raise `ValueError`. Standard library only, deterministic, and no
filesystem/network/global state. Examples: `"1" -> 1`, `"008" -> 8`;
`" 8"`, `"8.0"`, `"+8"`, `"0"`, and `"100001"` are invalid.

Acceptance: helper edge tests, benchmark-loader integration tests, full ANVIL
tests and validation.

## Task C — calculation / classification

Useful feature: classify an evaluated attempt for concise operational metrics.

Engineer scope: `anvil/metrics.py`, `tests/test_metrics.py`, and task-C raw
evidence. Integrate the helper in a small existing metrics-facing path only if
the existing interfaces support it without changing unrelated semantics.

Qwen subtask:

```python
classify_success_rate(accepted: int, samples: int) -> str
```

Both arguments must be `int` and not `bool`; `samples` must be positive and
`accepted` must be in `[0, samples]`; invalid input raises `ValueError`.
Return `"none"` for zero accepted, `"partial"` for accepted below samples,
and `"complete"` when accepted equals samples. Standard library only; no
filesystem/network/global state. Examples: `(0, 4) -> "none"`, `(2, 4) ->
"partial"`, `(4, 4) -> "complete"`.

Acceptance: boundary/invalid tests, integration tests if applicable, full ANVIL
tests and validation.

## Task D — transformation / rendering

Useful feature: safely render untrusted failure labels in the existing Markdown
summary without changing other report content.

Engineer scope: `anvil/reporting.py`, `tests/test_reporting.py`, and task-D
raw evidence. Integrate the accepted helper when rendering failure-mode list
items.

Qwen subtask:

```python
escape_markdown_text(value: str) -> str
```

Require a `str` and reject other types with `ValueError`. Escape backslash
first, then Markdown-special characters `*`, `_`, `` ` ``, `[`, `]`, `(`, `)`
and `#` by prefixing each with one backslash. Preserve all other characters,
including newlines and Unicode; do not HTML-escape or trim. It must be
deterministic and have no filesystem/network/global state. Example:
`"bad_[x]*" -> "bad\\_\\[x\\]\\*"`.

Acceptance: exact escaping tests, summary integration tests, full ANVIL tests
and validation.

## Campaign acceptance

For each task Axiom independently checks scope, raw evidence, artifact versus
integrated code, tests, and unrelated drift. After all four trials, fresh
Auditors inspect the combined result. Production vLLM is checked on published
port 8010 before and after the one campaign window. No production routing or
serving configuration may change.
