Repair this existing function without changing its signature.

```python
def group_by_initial(words: list[str]) -> dict[str, list[str]]:
    result = {}
    for word in words:
        result[word[0]] = [word]
    return result
```

Contract: return a dictionary mapping each word's first character to a list of all words with that initial, in original order. Input is a list of nonempty strings.

Observed failing evidence: `group_by_initial(["apple", "ant"])` returned `{"a": ["ant"]}`; expected `{"a": ["apple", "ant"]}`.
