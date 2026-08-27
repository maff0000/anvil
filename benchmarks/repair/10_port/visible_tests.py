def run_tests(fn):
    failures = []
    for arg in ["0", "65536", "abc"]:
        try:
            fn(arg)
            failures.append(f"expected: ValueError actual: returned value for {arg!r}")
        except ValueError:
            pass
    return {"passed": 3 - len(failures), "failed": len(failures), "failures": failures}
