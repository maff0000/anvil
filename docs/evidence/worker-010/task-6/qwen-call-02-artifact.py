import decimal

def format_failure_rate(failures: int, samples: int) -> str:
    if not isinstance(failures, int) or isinstance(failures, bool):
        raise ValueError("failures must be an integer")
    if not isinstance(samples, int) or isinstance(samples, bool):
        raise ValueError("samples must be an integer")
    if samples <= 0:
        raise ValueError("samples must be positive")
    if failures < 0 or failures > samples:
        raise ValueError("failures must be in [0, samples]")
    decimal.getcontext().rounding = decimal.ROUND_HALF_EVEN
    fail = decimal.Decimal(failures)
    total = decimal.Decimal(samples)
    rate = (fail / total * 100).quantize(decimal.Decimal("0.1"))
    return f"{rate}%"
