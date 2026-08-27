from dataclasses import dataclass
import ast
import base64
import json
import subprocess
import sys
import tempfile
from pathlib import Path


@dataclass(frozen=True)
class Evaluation:
    syntactic_validity: bool
    semantic_pass: bool
    tests: dict[str, object]
    error: str | None = None


def extract_python(text: str) -> str:
    candidates = []
    lines = text.splitlines()
    in_fence = False
    current: list[str] = []
    for line in lines:
        if line.strip().startswith("```"):
            if in_fence:
                candidates.append("\n".join(current).strip())
                current = []
            in_fence = not in_fence
        elif in_fence:
            current.append(line)
    if not candidates and text.strip():
        candidates.append(text.strip())
    for candidate in candidates:
        try:
            tree = ast.parse(candidate)
        except SyntaxError:
            continue
        if any(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "slugify" for node in tree.body):
            return candidate
    raise ValueError("no mechanically extractable slugify implementation")


def evaluate(text: str, reference_tests: Path, timeout_seconds: float = 5.0) -> Evaluation:
    try:
        artifact = extract_python(text)
        compile(artifact, "<generated>", "exec")
    except (SyntaxError, ValueError) as exc:
        return Evaluation(False, False, {"passed": 0, "failed": 0}, str(exc))
    tests = reference_tests.read_text(encoding="utf-8")
    payload = base64.b64encode((artifact + "\n" + tests).encode()).decode()
    script = """import base64, json, resource
resource.setrlimit(resource.RLIMIT_CPU, (2, 2))
resource.setrlimit(resource.RLIMIT_FSIZE, (65536, 65536))
source = base64.b64decode(%r).decode()
def safe_import(name, globals=None, locals=None, fromlist=(), level=0):
    if name == 're':
        return __import__('re', globals, locals, fromlist, level)
    raise ImportError('imports are not permitted in generated code')
namespace = {'__builtins__': {'str': str, 'isinstance': isinstance, 'int': int, 'ValueError': ValueError, 'Exception': Exception, 'TypeError': TypeError, 'len': len, 'range': range, 'ord': ord, 'chr': chr, 'list': list, 'tuple': tuple, 'dict': dict, 'all': all, 'any': any, 'type': type, 'filter': filter, 'map': map, 'zip': zip, 'sorted': sorted, 'min': min, 'max': max, '__import__': safe_import}}
exec(compile(source, '<generated>', 'exec'), namespace)
exec(compile('result = run_tests(slugify)', '<tests>', 'exec'), namespace)
print(json.dumps(namespace['result']))
""" % payload
    with tempfile.TemporaryDirectory(prefix="anvil-eval-") as directory:
        try:
            completed = subprocess.run([sys.executable, "-I", "-S", "-c", script], cwd=directory, env={}, capture_output=True, text=True, timeout=timeout_seconds)
        except subprocess.TimeoutExpired:
            return Evaluation(True, False, {"passed": 0, "failed": 0}, "evaluation_timeout")
    if completed.returncode != 0:
        return Evaluation(True, False, {"passed": 0, "failed": 0}, completed.stderr[-1000:] or "evaluation_failed")
    try:
        result = json.loads(completed.stdout)
    except json.JSONDecodeError:
        return Evaluation(True, False, {"passed": 0, "failed": 0}, "invalid_evaluator_output")
    return Evaluation(True, bool(result.get("failed", 1) == 0), result)
