def run_tests(fn):
    cases = [([], []), ([" Python ", "python", " ", "AI"], ["python", "ai"]), (["A", " b ", "B"], ["a", "b"]), (["x", "x"], ["x"])]
    failures = [f"{arg!r}: {fn(arg)!r} != {expected!r}" for arg, expected in cases if fn(arg) != expected]
    return {"passed": len(cases) - len(failures), "failed": len(failures), "failures": failures}
