Repair this existing function without changing its signature.

```python
def days_in_month(year: int, month: int) -> int:
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return days[month - 1]
```

Contract: return the number of days in the given Gregorian calendar month. February has 29 days in leap years (divisible by 4, except century years unless divisible by 400). Month is 1 through 12 and year is positive.

Observed failing evidence: `days_in_month(2024, 2)` returned 28; expected 29.
