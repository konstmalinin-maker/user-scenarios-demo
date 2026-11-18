"""C: сервис проверяется отдельно с mock-портом, без файлов/БД."""

from unittest.mock import create_autospec

import pytest

from src.domain.exceptions import NoteNotFoundError, StorageError, ValidationError
from src.domain.note import Note
from src.domain.ports import INoteStorage
from src.domain.service import NoteService


@pytest.fixture
def pair():
    mock = create_autospec(INoteStorage, instance=True)
    mock.load_all.return_value = []
    return NoteService(mock), mock


def test_constructor_and_add(pair):
    service, mock = pair
    note = service.add(" А ", " Б ")
    mock.load_all.assert_called_once_with()
    mock.save_all.assert_called_once_with([note])
    assert note.title == "А" and note.body == "Б"


def test_validation_before_io(pair):
    service, mock = pair
    with pytest.raises(ValidationError):
        service.add("", "Б")
    mock.load_all.assert_not_called()
    mock.save_all.assert_not_called()


def test_read_methods_do_not_save(pair):
    service, mock = pair
    n = Note.new("Покупки", "Б")
    mock.load_all.return_value = [n]
    assert service.list() == [n]
    assert service.search("ПОКУПКИ") == [n]
    assert service.get(n.id) == n
    mock.save_all.assert_not_called()


def test_missing_get(pair):
    service, _ = pair
    with pytest.raises(NoteNotFoundError):
        service.get("unknown")


def test_mock_edit_does_not_mutate_loaded_snapshot(pair):
    service, mock = pair
    old = Note.new("А", "Б")
    snapshot = [old]
    mock.load_all.return_value = snapshot
    mock.save_all.side_effect = StorageError("disk")
    with pytest.raises(StorageError):
        service.edit(old.id, title="В")
    assert snapshot == [old] and old.title == "А"


def test_delete_contract(pair):
    service, mock = pair
    n = Note.new("А", "Б")
    mock.load_all.return_value = [n]
    service.delete(n.id)
    mock.save_all.assert_called_once_with([])
