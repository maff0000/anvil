def run_tests(fn):
    failures = []
    for arg, expected in [("1", 1), (" 8080 ", 8080), ("65535", 65535)]:
        try:
            actual = fn(arg)
            if actual != expected:
                failures.append(f"{arg!r}: {actual!r} != {expected!r}")
        except Exception as exc:
            failures.append(f"{arg!r}: unexpected {type(exc).__name__}")
    for arg in ["", "0", "65536", "abc", "12.5", "-1"]:
        try:
            fn(arg)
            failures.append(f"{arg!r}: expected ValueError")
        except ValueError:
            pass
        except Exception as exc:
            failures.append(f"{arg!r}: wrong exception {type(exc).__name__}")
    return {"passed": 9 - len(failures), "failed": len(failures), "failures": failures}
