Repair this existing function without changing its signature.

```python
def sort_scores(scores: list[int]) -> list[int]:
    return sorted(scores)
```

Contract: return a new list containing the same scores sorted from highest to lowest. Do not mutate the input list. Equal values remain equal.

Observed failing evidence: `sort_scores([3, 1, 2])` returned `[1, 2, 3]`; expected `[3, 2, 1]`.
