"""G: каждый тест SC-001..SC-005 выполняется на двух адаптерах."""

import pytest

from src.infrastructure.sqlite_storage import SQLiteNoteStorage
from src.infrastructure.storage import NoteStorage


@pytest.fixture(params=["json", "sqlite"])
def storage(request, tmp_path):
    if request.param == "sqlite":
        return SQLiteNoteStorage(tmp_path / "notes.sqlite3")
    return NoteStorage(tmp_path / "notes.json")
