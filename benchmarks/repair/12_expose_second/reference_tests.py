def run_tests(fn):
    cases = [([], {}), (["a"], {"a": 1}), (["a", "a", "b"], {"a": 2, "b": 1}), (["x", "x", "x"], {"x": 3}), (["b", "a", "b", "c", "a"], {"a": 2, "b": 2, "c": 1})]
    failures = [f"{arg!r}: {fn(arg)!r} != {expected!r}" for arg, expected in cases if fn(arg) != expected]
    return {"passed": len(cases) - len(failures), "failed": len(failures), "failures": failures}
