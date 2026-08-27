def run_tests(fn):
    cases = [((10, 0, 10), 10), ((-1, 0, 10), 0)]
    failures = [f"expected: {expected!r} actual: {fn(*args)!r}" for args, expected in cases if fn(*args) != expected]
    return {"passed": len(cases) - len(failures), "failed": len(failures), "failures": failures}
