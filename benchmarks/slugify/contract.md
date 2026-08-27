# Slugify contract

Implement exactly `def slugify(value: str) -> str`.

- Input is a Python `str`; output is lowercase.
- Remove surrounding whitespace.
- Every run of non-ASCII-alphanumeric characters becomes one `-`.
- Repeated separators collapse; remove leading/trailing `-`.
- ASCII digits remain. Empty or punctuation-only input returns `""`.
- No external dependencies, filesystem/network/global state, or nondeterminism.

