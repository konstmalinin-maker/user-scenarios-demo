"""B: интеграция через реальные subprocess; все пять команд, два адаптера."""

import os
import re
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.fixture(params=["json", "sqlite"])
def cli(request, tmp_path):
    env = {**os.environ, "NOTES_BACKEND": request.param, "NOTES_PATH": str(tmp_path / "notes")}

    def run(*args, text=""):
        return subprocess.run(
            [sys.executable, "-m", "src.cli", *args],
            input=text,
            capture_output=True,
            text=True,
            env=env,
            cwd=Path(__file__).resolve().parents[1],
            timeout=10,
        )

    return run


def added(cli):
    result = cli("add", "--title", "Покупки", "--body", "Молоко")
    assert result.returncode == 0, result.stderr
    return re.search(r"[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}", result.stdout).group()


def test_five_commands(cli):
    assert "Заметок пока нет" in cli("list").stdout
    note_id = added(cli)
    assert note_id in cli("list").stdout
    assert "Покупки" in cli("search", "--query", "МОЛОКО").stdout
    assert cli("edit", note_id, "--title", "Новые покупки").returncode == 0
    assert "Новые покупки" in cli("list").stdout
    assert "удалена" in cli("delete", note_id, text="да\n").stdout
    assert "Заметок пока нет" in cli("list").stdout


def test_no_matches(cli):
    assert "Ничего не найдено" in cli("search", "--query", "нет").stdout


@pytest.mark.parametrize(
    "command", [("add", "--title", "", "--body", "Б"), ("search", "--query", " ")]
)
def test_invalid_input(cli, command):
    result = cli(*command)
    assert result.returncode == 2 and "Ошибка" in result.stderr
    assert "Traceback" not in result.stderr


@pytest.mark.parametrize("answer", ["нет\n", "no\n", "", "что-то\n"])
def test_delete_cancel_or_eof(cli, answer):
    note_id = added(cli)
    result = cli("delete", note_id, text=answer)
    assert result.returncode == 0
    assert note_id in cli("list").stdout


@pytest.mark.parametrize("command", ["edit", "delete"])
def test_unknown_before_prompt(cli, command):
    result = cli(command, "missing")
    assert result.returncode == 2
    assert "не найдена" in result.stderr
    assert "[да/нет]" not in result.stdout and "Новый" not in result.stdout


def test_edit_enter_noop(cli):
    note_id = added(cli)
    before = cli("list").stdout
    assert cli("edit", note_id, text="\n\n").returncode == 0
    assert cli("list").stdout == before


def test_edit_interactive(cli):
    note_id = added(cli)
    assert cli("edit", note_id, text="Другое\nТекст\n").returncode == 0
    assert "Другое" in cli("list").stdout


def test_edit_explicit_empty_invalid(cli):
    note_id = added(cli)
    assert cli("edit", note_id, "--title", "").returncode == 2
    assert "Покупки" in cli("list").stdout


def test_interactive_retry(cli):
    result = cli("add", text="\nБ\nА\nБ\n")
    assert result.returncode == 0 and "добавлена" in result.stdout
    assert "Повторите" in result.stderr


def test_interactive_empty_body_retry(cli):
    result = cli("add", text="А\n\nА\nБ\n")
    assert result.returncode == 0 and "Повторите" in result.stderr


def test_interactive_eof(cli):
    assert "отменена" in cli("add").stdout


def test_help(cli):
    result = cli("--help")
    assert result.returncode == 0 and "search" in result.stdout


def test_argparse_error(cli):
    assert cli("search").returncode == 2


def test_bad_backend(monkeypatch, cli):
    env = {**os.environ, "NOTES_BACKEND": "bad"}
    result = subprocess.run(
        [sys.executable, "-m", "src.cli", "list"],
        env=env,
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 2 and "NOTES_BACKEND" in result.stderr
