def run_tests(fn):
    cases = [((False, False), False), ((True, False), True), ((False, True), True), ((True, True), True)]
    failures = [f"{args}: {fn(*args)!r} != {expected!r}" for args, expected in cases if fn(*args) != expected]
    return {"passed": len(cases) - len(failures), "failed": len(failures), "failures": failures}
