def run_tests(fn):
    cases = [([], []), (["a"], ["a"]), (["a", "b", "a", "c", "b"], ["a", "b", "c"]), (["x", "x", "x"], ["x"]), (["b", "a"], ["b", "a"])]
    failures = [f"{arg!r}: {fn(arg)!r} != {expected!r}" for arg, expected in cases if fn(arg) != expected]
    return {"passed": len(cases) - len(failures), "failed": len(failures), "failures": failures}
