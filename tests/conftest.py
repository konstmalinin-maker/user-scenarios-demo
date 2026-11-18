"""Общий контракт хранилища для сценарных тестов."""

import pytest

from src.infrastructure.storage import NoteStorage


@pytest.fixture(params=["json"])
def storage(request, tmp_path):
    return NoteStorage(tmp_path / "notes.json")
