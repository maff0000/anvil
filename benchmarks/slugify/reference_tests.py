def run_tests(slugify):
    cases = {
        "Hello World": "hello-world", "  Hello   World  ": "hello-world",
        "Hello, world!": "hello-world", "foo___bar": "foo-bar",
        "---Hello---": "hello", "Version 2 Build 17": "version-2-build-17",
        "": "", " !!! ": "", "A.B/C": "a-b-c", "99 bottles": "99-bottles",
        "  already--slug  ": "already-slug", "a\tb\nc": "a-b-c",
        "éclair": "clair", "中文": "", "a   b___c": "a-b-c",
    }
    passed = 0
    failures = []
    for value, expected in cases.items():
        try:
            actual = slugify(value)
            if actual == expected:
                passed += 1
            else:
                failures.append({"input": value, "expected": expected, "actual": actual})
        except Exception as exc:
            failures.append({"input": value, "expected": expected, "error": type(exc).__name__ + ": " + str(exc)})
    return {"passed": passed, "failed": len(failures), "total": len(cases), "failures": failures}

