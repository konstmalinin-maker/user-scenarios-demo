"""Контракт сущности и атомарного JSON-адаптера."""

import json
from unittest.mock import patch

import pytest

from src.domain.exceptions import StorageError
from src.domain.note import Note
from src.infrastructure.storage import NoteStorage


@pytest.mark.parametrize("payload", ["{", "{}", "[{}]", "[1]", '[{"id": 1}]'])
def test_corrupt_json(tmp_path, payload):
    path = tmp_path / "data.json"
    path.write_text(payload)
    with pytest.raises(StorageError):
        NoteStorage(path).load_all()


def test_note_roundtrip():
    n = Note.new("А", "Б")
    assert Note.from_dict(n.to_dict()) == n


def test_naive_date():
    data = Note.new("А", "Б").to_dict()
    data["created_at"] = "2026-01-01T00:00:00"
    with pytest.raises(ValueError, match="часовой"):
        Note.from_dict(data)


def test_duplicate_rejected(tmp_path):
    s = NoteStorage(tmp_path / "data.json")
    n = Note.new("А", "Б")
    s.save_all([n])
    with pytest.raises(StorageError):
        s.save_all([n, n])
    assert s.load_all() == [n]
    s.path.write_text(json.dumps([n.to_dict(), n.to_dict()]))
    with pytest.raises(StorageError):
        s.load_all()


def test_replace_failure_atomic(tmp_path):
    s = NoteStorage(tmp_path / "data.json")
    n = Note.new("А", "Б")
    s.save_all([n])
    before = s.path.read_bytes()
    with patch("src.infrastructure.storage.os.replace", side_effect=OSError("disk")):
        with pytest.raises(StorageError, match="записи"):
            s.save_all([])
    assert s.path.read_bytes() == before
    assert not list(tmp_path.glob("*.tmp"))


def test_missing_directory(tmp_path):
    with pytest.raises(StorageError):
        NoteStorage(tmp_path / "missing" / "a.json").save_all([])
