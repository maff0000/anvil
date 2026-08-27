def run_tests(fn):
    cases = [("abc", True), ("A9", True), ("", False), ("abc123", True), ("café", False), ("１２", False), ("a_b", False), (" ", False)]
    failures = [f"{arg!r}: {fn(arg)!r} != {expected!r}" for arg, expected in cases if fn(arg) != expected]
    return {"passed": len(cases) - len(failures), "failed": len(failures), "failures": failures}
