def run_tests(fn):
    expected = ["a", "b", "c"]
    actual = fn(["a", "b", "a", "c", "b"])
    failures = [] if actual == expected else [f"expected: {expected!r} actual: {actual!r}"]
    return {"passed": 1 - len(failures), "failed": len(failures), "failures": failures}
