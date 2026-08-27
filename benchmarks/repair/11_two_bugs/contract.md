Repair this existing function without changing its signature.

```python
def clean_tags(tags: list[str]) -> list[str]:
    return [tag.strip() for tag in tags if tag]
```

Contract: trim whitespace, lowercase each tag, discard empty results, and remove duplicate tags while preserving first occurrence order.

Observed failing evidence: `clean_tags([" Python ", "python", " "])` returned `["Python", "python"]`; expected `["python"]`.
