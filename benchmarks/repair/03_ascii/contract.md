Repair this existing function without changing its signature.

```python
def is_ascii_word(value: str) -> bool:
    return bool(value) and value.isalnum()
```

Contract: return True only when value is nonempty and every character is an ASCII letter or ASCII digit. Unicode letters and digits are not ASCII. Input is a string.

Observed failing evidence: `is_ascii_word("café")` returned True; expected False.
