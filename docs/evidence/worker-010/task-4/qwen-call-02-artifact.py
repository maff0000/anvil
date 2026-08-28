def parse_passed_total(value: str) -> tuple[int, int]:
    if not isinstance(value, str):
        raise ValueError("Input must be a string")

    parts = value.split('/')
    if len(parts) != 2:
        raise ValueError("Must contain exactly one slash")

    num_str, denom_str = parts

    for s in [num_str, denom_str]:
        if not s:
            raise ValueError("Numerator or denominator cannot be empty")
        for ch in s:
            if ord(ch) < 48 or ord(ch) > 57:
                raise ValueError(f"Invalid character in number: {ch!r}")

    numerator = int(num_str)
    denominator = int(denom_str)

    if denominator <= 0:
        raise ValueError("Denominator must be positive")
    if numerator > denominator:
        raise ValueError("Numerator cannot exceed denominator")
    if numerator > 100000 or denominator > 100000:
        raise ValueError("Values exceed maximum of 100000")

    return (numerator, denominator)
