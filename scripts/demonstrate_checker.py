"""Сохранить реальные exit codes E; повреждается только временная копия."""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

source = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as folder:
    root = Path(folder)
    for name in ("docs", "src", "tests"):
        shutil.copytree(
            source / name,
            root / name,
            ignore=shutil.ignore_patterns("__pycache__", "evidence", "pr6-images"),
        )

    def run(label):
        result = subprocess.run(
            [sys.executable, str(source / "scripts/check_scenarios.py"), "--root", str(root)],
            text=True,
            capture_output=True,
            check=False,
        )
        print(f"{label}: exit={result.returncode}\n{result.stdout.strip()}")
        return result.returncode

    assert run("Корректный проект") == 0
    for name in ("src/scenarios/add_note.py", "tests/test_add_note.py"):
        path = root / name
        original = path.read_text()
        path.unlink()
        assert run(f"Удалён {name}") == 1
        path.write_text(original)
        path.write_text(original.replace("SC-001", "WRONG"))
        assert run(f"Убран SC-ID из {name}") == 1
        path.write_text(original)
    assert run("Восстановлено") == 0
