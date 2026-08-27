Repair this existing function without changing its signature.

```python
def summarize_counts(values: list[str]) -> dict[str, int]:
    result = {}
    for value in values:
        result[value] = 1
    return result
```

Contract: return a dictionary containing the count of every value. Repeated values increment their existing count. Values are strings.

Observed failing evidence: `summarize_counts(["a", "a"])` returned `{"a": 1}`; expected `{"a": 2}`.
