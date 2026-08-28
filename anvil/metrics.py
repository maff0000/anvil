"""Small deterministic metric helpers."""

from math import ceil, isfinite


def percentile(values: list[float], p: float) -> float:
    """Return the nearest-rank percentile of a non-empty finite sequence."""
    if not values:
        raise ValueError("values must be non-empty")
    if not isfinite(p) or not 0.0 <= p <= 1.0:
        raise ValueError("p must be between 0 and 1")

    ordered = sorted(values)
    if not all(isfinite(value) for value in ordered):
        raise ValueError("values must be finite")

    rank = 1 if p == 0.0 else ceil(p * len(ordered))
    rank = max(1, min(rank, len(ordered)))
    return float(ordered[rank - 1])
