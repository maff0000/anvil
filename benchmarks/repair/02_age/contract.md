Repair this existing function without changing its signature.

```python
def is_working_age(age: int) -> bool:
    return age > 18 and age < 65
```

Contract: return True exactly for ages from 18 through 65 inclusive, and False otherwise. Input is an integer.

Observed failing evidence: `is_working_age(18)` returned False; expected True.
