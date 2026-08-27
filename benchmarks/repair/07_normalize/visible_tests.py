def run_tests(fn):
    cases = [("  User   Name ", "user_name"), ("A\tB\nC", "a_b_c")]
    failures = [f"expected: {expected!r} actual: {fn(arg)!r}" for arg, expected in cases if fn(arg) != expected]
    return {"passed": len(cases) - len(failures), "failed": len(failures), "failures": failures}
