def run_tests(fn):
    cases = [([], {}), (["apple"], {"a": ["apple"]}), (["apple", "ant", "boat", "berry"], {"a": ["apple", "ant"], "b": ["boat", "berry"]}), (["X", "x"], {"X": ["X"], "x": ["x"]})]
    failures = [f"{arg!r}: {fn(arg)!r} != {expected!r}" for arg, expected in cases if fn(arg) != expected]
    return {"passed": len(cases) - len(failures), "failed": len(failures), "failures": failures}
