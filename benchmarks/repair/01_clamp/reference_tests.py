def run_tests(fn):
    cases = [((-2, 0, 10), 0), ((0, 0, 10), 0), ((5, 0, 10), 5), ((10, 0, 10), 10), ((12, 0, 10), 10), ((3, 3, 3), 3)]
    failures = [f"{args}: {fn(*args)!r} != {expected!r}" for args, expected in cases if fn(*args) != expected]
    return {"passed": len(cases) - len(failures), "failed": len(failures), "failures": failures}
