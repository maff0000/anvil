def run_tests(fn):
    cases = [("café", False), ("abc123", True)]
    failures = [f"expected: {expected!r} actual: {fn(arg)!r}" for arg, expected in cases if fn(arg) != expected]
    return {"passed": len(cases) - len(failures), "failed": len(failures), "failures": failures}
