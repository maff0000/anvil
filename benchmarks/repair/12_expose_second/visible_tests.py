def run_tests(fn):
    expected = {"a": 2, "b": 1}
    actual = fn(["a", "a", "b"])
    failures = [] if actual == expected else [f"expected: {expected!r} actual: {actual!r}"]
    return {"passed": 1 - len(failures), "failed": len(failures), "failures": failures}
