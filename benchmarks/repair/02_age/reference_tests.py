def run_tests(fn):
    cases = [(-1, False), (17, False), (18, True), (19, True), (64, True), (65, True), (66, False)]
    failures = [f"{arg}: {fn(arg)!r} != {expected!r}" for arg, expected in cases if fn(arg) != expected]
    return {"passed": len(cases) - len(failures), "failed": len(failures), "failures": failures}
