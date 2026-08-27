Repair this existing function without changing its signature.

```python
def unique_items(items: list[str]) -> list[str]:
    return list(set(items))
```

Contract: return the first occurrence of each item, preserving input order. Do not mutate the input. Items are strings.

Observed failing evidence: `unique_items(["a", "b", "a"])` did not preserve the required first-occurrence order.
