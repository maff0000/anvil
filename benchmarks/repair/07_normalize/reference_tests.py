def run_tests(fn):
    cases = [("", ""), (" User ", "user"), ("  User   Name ", "user_name"), ("A\tB\nC", "a_b_c"), ("hello-world", "hello-world"), ("  X  Y  Z  ", "x_y_z")]
    failures = [f"{arg!r}: {fn(arg)!r} != {expected!r}" for arg, expected in cases if fn(arg) != expected]
    return {"passed": len(cases) - len(failures), "failed": len(failures), "failures": failures}
