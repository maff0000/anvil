def run_tests(fn):
    values = [3, 1, 2]
    result = fn(values)
    failures = [] if result == [3, 2, 1] and values == [3, 1, 2] else [f"expected: [3, 2, 1] actual: {result!r}"]
    return {"passed": 1 - len(failures), "failed": len(failures), "failures": failures}
