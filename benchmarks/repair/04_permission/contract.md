Repair this existing function without changing its signature.

```python
def can_edit(is_owner: bool, is_admin: bool) -> bool:
    return is_owner and is_admin
```

Contract: an owner OR an administrator may edit. Return True if either flag is True, otherwise False. Inputs are booleans.

Observed failing evidence: `can_edit(True, False)` returned False; expected True.
