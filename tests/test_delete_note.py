"""SC-005: основной поток, альтернативы и ошибки сохранения."""

from unittest.mock import patch

import pytest

from src.domain.exceptions import NoteNotFoundError, StorageError
from src.scenarios.add_note import add_note
from src.scenarios.delete_note import delete_note


def test_delete_only(storage):
    n = add_note("А", "Б", storage)
    assert delete_note(n.id, storage) is None
    assert storage.load_all() == []


def test_preserve_other(storage):
    a, b = add_note("А", "Б", storage), add_note("В", "Г", storage)
    delete_note(a.id, storage)
    assert storage.load_all() == [b]


def test_unknown_empty(storage):
    with pytest.raises(NoteNotFoundError):
        delete_note("missing", storage)


def test_unknown_keeps_old(storage):
    old = add_note("А", "Б", storage)
    with pytest.raises(NoteNotFoundError):
        delete_note("missing", storage)
    assert storage.load_all() == [old]


def test_second_delete(storage):
    n = add_note("А", "Б", storage)
    delete_note(n.id, storage)
    with pytest.raises(NoteNotFoundError):
        delete_note(n.id, storage)


def test_write_failure(storage):
    old = add_note("А", "Б", storage)
    with patch.object(storage, "save_all", side_effect=StorageError("Ошибка записи")):
        with pytest.raises(StorageError):
            delete_note(old.id, storage)
    assert storage.load_all() == [old]


def test_read_failure(storage):
    with patch.object(storage, "load_all", side_effect=StorageError("Ошибка чтения")):
        with pytest.raises(StorageError):
            delete_note("missing", storage)


pytestmark = pytest.mark.scenario("SC-005")
