"""SC-004: основной поток, альтернативы и ошибки сохранения."""

from unittest.mock import patch

import pytest

from src.domain.exceptions import NoteNotFoundError, StorageError, ValidationError
from src.scenarios.add_note import add_note
from src.scenarios.edit_note import edit_note


def test_title_only(storage):
    old = add_note("А", "Б", storage)
    new = edit_note(old.id, storage, title=" В ")
    assert new.title == "В" and new.body == "Б"
    assert new.id == old.id and new.created_at == old.created_at
    assert new.updated_at >= old.updated_at
    assert storage.load_all() == [new]


def test_body_only(storage):
    old = add_note("А", "Б", storage)
    new = edit_note(old.id, storage, body=" Г ")
    assert new.title == "А" and new.body == "Г"


def test_both(storage):
    old = add_note("А", "Б", storage)
    assert edit_note(old.id, storage, "В", "Г").body == "Г"


def test_none_noop(storage):
    old = add_note("А", "Б", storage)
    with patch.object(storage, "save_all") as save:
        assert edit_note(old.id, storage) == old
    save.assert_not_called()


@pytest.mark.parametrize(
    "fields",
    [
        {"title": ""},
        {"title": " "},
        {"body": ""},
        {"body": " "},
        {"title": "А" * 101},
        {"body": "Б" * 10001},
    ],
)
def test_invalid_keeps_old(storage, fields):
    old = add_note("А", "Б", storage)
    with pytest.raises(ValidationError):
        edit_note(old.id, storage, **fields)
    assert storage.load_all() == [old]


def test_exact_maxima(storage):
    old = add_note("А", "Б", storage)
    new = edit_note(old.id, storage, "А" * 100, "Б" * 10000)
    assert len(new.title) == 100 and len(new.body) == 10000


def test_unknown(storage):
    with pytest.raises(NoteNotFoundError):
        edit_note("missing", storage, "В")


def test_other_note_preserved(storage):
    a, b = add_note("А", "Б", storage), add_note("В", "Г", storage)
    edit_note(b.id, storage, "Д")
    assert storage.load_all()[0] == a


def test_write_failure(storage):
    old = add_note("А", "Б", storage)
    with patch.object(storage, "save_all", side_effect=StorageError("Ошибка записи")):
        with pytest.raises(StorageError):
            edit_note(old.id, storage, "В")
    assert storage.load_all() == [old]


def test_read_failure(storage):
    with patch.object(storage, "load_all", side_effect=StorageError("Ошибка чтения")):
        with pytest.raises(StorageError):
            edit_note("missing", storage)


pytestmark = pytest.mark.scenario("SC-004")
