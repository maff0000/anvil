def parse_sample_count(value: str) -> int:
    if not isinstance(value, str):
        raise ValueError("Input must be a string")

    if not value:
        raise ValueError("Input cannot be empty")

    for char in value:
        if not ('0' <= char <= '9'):
            raise ValueError("Input must consist only of ASCII decimal digits")

    try:
        result = int(value)
    except ValueError:
        raise ValueError("Invalid integer format")

    if result < 1 or result > 100000:
        raise ValueError("Value must be between 1 and 100000 inclusive")

    return result
