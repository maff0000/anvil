def run_tests(fn):
    cases = [((2024, 2), 29), ((2023, 2), 28)]
    failures = [f"expected: {expected!r} actual: {fn(*args)!r}" for args, expected in cases if fn(*args) != expected]
    return {"passed": len(cases) - len(failures), "failed": len(failures), "failures": failures}
