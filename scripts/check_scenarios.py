"""E: проверка сценарий → docstring модуля → настоящий тест."""

import argparse
import ast
import json
import re
from pathlib import Path


def check(root: Path) -> list[str]:
    errors = []
    records = json.loads((root / "docs/scenarios.json").read_text(encoding="utf8"))
    declared = set(
        re.findall(
            r"^## (SC-\d{3})\b",
            (root / "docs/scenarios.md").read_text(encoding="utf8"),
            re.MULTILINE,
        )
    )
    if declared != {r["id"] for r in records}:
        errors.append("docs/scenarios.md и scenarios.json содержат разные SC-ID")
    for r in records:
        for kind in ("module", "test"):
            path = root / r[kind]
            if not path.is_file():
                errors.append(f"{r['id']}: отсутствует {r[kind]}")
                continue
            try:
                tree = ast.parse(path.read_text(encoding="utf8"))
            except SyntaxError:
                errors.append(f"{r['id']}: синтаксическая ошибка {r[kind]}")
                continue
            if r["id"] not in (ast.get_docstring(tree) or ""):
                errors.append(f"{r['id']}: нет ID в docstring {r[kind]}")
            if r["status"] == "implemented":
                if kind == "test" and not any(
                    isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                    and n.name.startswith("test_")
                    for n in ast.walk(tree)
                ):
                    errors.append(f"{r['id']}: нет тестовых функций")
                if kind == "module" and any(
                    isinstance(n, ast.Name) and n.id == "NotImplementedError"
                    for n in ast.walk(tree)
                ):
                    errors.append(f"{r['id']}: осталась заглушка")
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    errors = check(parser.parse_args().root)
    print("\n".join(errors) if errors else "OK: все 5 сценариев связаны с модулями и тестами")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
