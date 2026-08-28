def classify_success_rate(accepted: int, samples: int) -> str:
    if not isinstance(accepted, int) or isinstance(accepted, bool):
        raise ValueError("accepted must be an integer and not a boolean")
    if not isinstance(samples, int) or isinstance(samples, bool):
        raise ValueError("samples must be an integer and not a boolean")
    if samples <= 0:
        raise ValueError("samples must be positive")
    if accepted < 0 or accepted > samples:
        raise ValueError("accepted must be in [0, samples]")

    if accepted == 0:
        return "none"
    elif accepted < samples:
        return "partial"
    else:
        return "complete"
