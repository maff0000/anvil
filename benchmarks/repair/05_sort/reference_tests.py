def run_tests(fn):
    original = [3, 1, 2]
    cases = [([], []), ([3, 1, 2], [3, 2, 1]), ([2, 2, 1], [2, 2, 1]), ([-1, 4, 0], [4, 0, -1])]
    failures = []
    for arg, expected in cases:
        before = list(arg)
        if fn(arg) != expected or arg != before:
            failures.append(f"{arg!r}: result/input mutation")
    if fn(original) != [3, 2, 1] or original != [3, 1, 2]:
        failures.append("input was mutated")
    return {"passed": len(cases) - min(len(failures), len(cases)), "failed": len(failures), "failures": failures}
