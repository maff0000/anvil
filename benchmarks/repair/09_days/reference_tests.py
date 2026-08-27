def run_tests(fn):
    cases = [((2024, 2), 29), ((2023, 2), 28), ((1900, 2), 28), ((2000, 2), 29), ((2024, 4), 30), ((2024, 12), 31)]
    failures = [f"{args}: {fn(*args)!r} != {expected!r}" for args, expected in cases if fn(*args) != expected]
    return {"passed": len(cases) - len(failures), "failed": len(failures), "failures": failures}
