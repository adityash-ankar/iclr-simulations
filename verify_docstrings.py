import ast
import os

root = os.path.join('code', 'electronic_pressure_regulator')
errors = []

for dirpath, _, filenames in os.walk(root):
    for fn in filenames:
        if fn.endswith('.py'):
            path = os.path.join(dirpath, fn)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    src = f.read()
                tree = ast.parse(src, filename=path)
            except Exception as exc:
                errors.append(f'{os.path.relpath(path, root)} parse-error: {exc}')
                continue
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    if ast.get_docstring(node) is None:
                        errors.append(f'{os.path.relpath(path, root)}:{node.lineno}:{type(node).__name__}:{node.name} missing docstring')

print('RESULT')
if errors:
    print('\n'.join(errors))
    raise SystemExit(1)
print('All function and class docstrings are present.')
