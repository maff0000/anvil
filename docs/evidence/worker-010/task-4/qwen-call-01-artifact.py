def parse_passed_total(value: str) -> tuple[int, int]:
    if not isinstance(value, str):
        raise ValueError("Input must be a string")
    if not value:
        raise ValueError("Input cannot be empty")
    parts = value.split('/')
    if len(parts) != 2:
        raise ValueError("Invalid format: expected exactly one slash")
    num_str, den_str = parts[0], parts[1]
    if not num_str or not den_str:
        raise ValueError("Numerator and denominator cannot be empty")
    if not num_str.isdigit() or not den_str.isdigit():
        raise ValueError("Numerator and denominator must contain only digits")
    numerator = int(num_str)
    denominator = int(den_str)
    if denominator <= 0:
        raise ValueError("Denominator must be positive")
    if numerator < 0 or numerator > denominator:
        raise ValueError("Numerator must be between 0 and denominator inclusive")
    if numerator > 100000 or denominator > 100000:
        raise ValueError("Counts must not exceed 100000")
    return (numerator, denominator)
