Repair this existing function without changing its signature.

```python
def normalize_key(value: str) -> str:
    return value.lower()
```

Contract: strip surrounding whitespace, lowercase, and replace every run of internal whitespace with one underscore. Input is a string; punctuation other than whitespace is preserved.

Observed failing evidence: `normalize_key("  User   Name ")` returned `"  user   name "`; expected `"user_name"`.
