def run_tests(fn):
    expected = ["python"]
    actual = fn([" Python ", "python", " "])
    failures = [] if actual == expected else [f"expected: {expected!r} actual: {actual!r}"]
    return {"passed": 1 - len(failures), "failed": len(failures), "failures": failures}
