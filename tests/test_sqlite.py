"""G: настоящая транзакция и повреждённая БД."""

import sqlite3
from contextlib import closing

import pytest

from src.domain.exceptions import StorageError, ValidationError
from src.domain.note import Note
from src.infrastructure.factory import create_storage
from src.infrastructure.sqlite_storage import SQLiteNoteStorage
from src.infrastructure.storage import NoteStorage


def test_sqlite_rollback(tmp_path):
    s = SQLiteNoteStorage(tmp_path / "n.sqlite3")
    n = Note.new("А", "Б")
    s.save_all([n])
    with pytest.raises(StorageError, match="записи"):
        s.save_all([n, n])
    assert s.load_all() == [n]


def test_broken_database(tmp_path):
    path = tmp_path / "n.sqlite3"
    path.write_bytes(b"this is not sqlite")
    s = SQLiteNoteStorage(path)
    with pytest.raises(StorageError, match="чтения"):
        s.load_all()
    with pytest.raises(StorageError, match="записи"):
        s.save_all([])


def test_invalid_record(tmp_path):
    s = SQLiteNoteStorage(tmp_path / "n.sqlite3")
    s.save_all([])
    with closing(sqlite3.connect(s.path)) as db, db:
        db.execute("INSERT INTO notes VALUES (?, ?)", ("bad", "{}"))
    with pytest.raises(StorageError):
        s.load_all()


@pytest.mark.parametrize("backend,cls", [("json", NoteStorage), (" SQLITE ", SQLiteNoteStorage)])
def test_factory_env(monkeypatch, tmp_path, backend, cls):
    monkeypatch.setenv("NOTES_BACKEND", backend)
    monkeypatch.setenv("NOTES_PATH", str(tmp_path / "notes"))
    assert isinstance(create_storage(), cls)


def test_factory_default(monkeypatch):
    monkeypatch.delenv("NOTES_BACKEND", raising=False)
    monkeypatch.delenv("NOTES_PATH", raising=False)
    assert isinstance(create_storage(), NoteStorage)


def test_factory_invalid(monkeypatch):
    monkeypatch.setenv("NOTES_BACKEND", "other")
    with pytest.raises(ValidationError):
        create_storage()
