Repair this existing function without changing its signature.

```python
def clamp(value: int, low: int, high: int) -> int:
    return max(low, min(value, high - 1))
```

Contract: return `value` constrained to the inclusive interval `[low, high]`. If value is below low return low; if above high return high. Inputs are integers and low <= high.

Observed failing evidence: `clamp(10, 0, 10)` returned 9; expected 10.
