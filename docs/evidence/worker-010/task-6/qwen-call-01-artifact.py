import decimal
from decimal import Decimal, ROUND_HALF_EVEN

def format_failure_rate(failures: int, samples: int) -> str:
    if not isinstance(failures, bool) or not isinstance(samples, bool):
        raise ValueError("Inputs must be integers (and not booleans).")
    if type(failures) is not int or type(samples) is not int:
        raise ValueError("Inputs must be integers.")
    if samples <= 0:
        raise ValueError("Samples must be positive.")
    if failures < 0 or failures > samples:
        raise ValueError("Failures must be in range [0, samples].")
    context = decimal.getcontext()
    context.rounding = ROUND_HALF_EVEN
    rate = Decimal(failures) / Decimal(samples) * 100
    quantized_rate = rate.quantize(Decimal("0.1"))
    return f"{quantized_rate}%"
