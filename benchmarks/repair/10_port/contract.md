Repair this existing function without changing its signature.

```python
def parse_port(value: str) -> int:
    return int(value)
```

Contract: strip surrounding whitespace, parse a base-10 integer, and return it only when it is between 1 and 65535 inclusive. For empty, non-numeric, or out-of-range input raise ValueError. Input is a string.

Observed failing evidence: `parse_port("0")` returned 0; expected ValueError.
