"""E: положительная проверка и реальные нарушения временной копии проекта."""

import shutil
from pathlib import Path

import pytest

from scripts.check_scenarios import check


@pytest.fixture
def root(tmp_path):
    source = Path(__file__).resolve().parents[1]
    for folder in ("docs", "src", "tests"):
        shutil.copytree(
            source / folder,
            tmp_path / folder,
            ignore=shutil.ignore_patterns("__pycache__", "pr6-images", "evidence"),
        )
    return tmp_path


def test_correct_project(root):
    assert check(root) == []


@pytest.mark.parametrize(
    "mode",
    [
        "module_missing",
        "test_missing",
        "module_docstring",
        "test_docstring",
        "no_tests",
        "syntax",
        "unknown_id",
        "stub",
    ],
)
def test_violation(root, mode):
    module = root / "src/scenarios/add_note.py"
    test = root / "tests/test_add_note.py"
    if mode == "module_missing":
        module.unlink()
    elif mode == "test_missing":
        test.unlink()
    elif mode == "module_docstring":
        module.write_text('"""Wrong ID."""\ndef add_note(): pass\n')
    elif mode == "test_docstring":
        test.write_text('"""Wrong ID."""\ndef test_add(): pass\n')
    elif mode == "no_tests":
        test.write_text('"""SC-001: no tests."""\n')
    elif mode == "syntax":
        module.write_text("def broken(:")
    elif mode == "unknown_id":
        doc = root / "docs/scenarios.md"
        doc.write_text(doc.read_text() + "\n## SC-999: forgotten scenario\n")
    else:
        module.write_text(module.read_text() + "\ndef forgotten(): raise NotImplementedError()\n")
    assert check(root), mode
