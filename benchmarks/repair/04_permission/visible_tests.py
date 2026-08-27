def run_tests(fn):
    cases = [((True, False), True), ((False, True), True)]
    failures = [f"expected: {expected!r} actual: {fn(*args)!r}" for args, expected in cases if fn(*args) != expected]
    return {"passed": len(cases) - len(failures), "failed": len(failures), "failures": failures}
