"""SC-001: основной поток, границы, UUID, ошибки, сохранность."""

from datetime import UTC, datetime
from unittest.mock import patch
from uuid import UUID

import pytest

from src.domain.exceptions import StorageError, ValidationError
from src.scenarios.add_note import add_note, validate_body, validate_title

pytestmark = pytest.mark.scenario("SC-001")


def test_add_persists(storage):
    note = add_note("Покупки", "Молоко", storage)
    assert storage.load_all() == [note]


def test_title_trimmed(storage):
    assert add_note("  А  ", "Б", storage).title == "А"


def test_body_trimmed(storage):
    assert add_note("А", "  Б  ", storage).body == "Б"


def test_empty_title(storage):
    with pytest.raises(ValidationError, match="Заголовок"):
        add_note("", "Б", storage)
    assert storage.load_all() == []


def test_whitespace_title(storage):
    with pytest.raises(ValidationError):
        add_note(" \n\t", "Б", storage)


def test_title_one(storage):
    assert add_note("А", "Б", storage).title == "А"


def test_title_max(storage):
    assert len(add_note("А" * 100, "Б", storage).title) == 100


def test_title_over_max(storage):
    with pytest.raises(ValidationError, match="100"):
        add_note("А" * 101, "Б", storage)


def test_empty_body(storage):
    with pytest.raises(ValidationError, match="Тело"):
        add_note("А", "", storage)


def test_whitespace_body(storage):
    with pytest.raises(ValidationError):
        add_note("А", " \n\t", storage)


def test_body_one(storage):
    assert add_note("А", "Б", storage).body == "Б"


def test_body_max(storage):
    assert len(add_note("А", "Б" * 10000, storage).body) == 10000


def test_body_over_max(storage):
    with pytest.raises(ValidationError, match="10000"):
        add_note("А", "Б" * 10001, storage)


def test_unique_uuid(storage):
    a, b = add_note("А", "Б", storage), add_note("А", "Б", storage)
    assert UUID(a.id).version == 4 and a.id != b.id


def test_time_utc(storage):
    before = datetime.now(UTC)
    note = add_note("А", "Б", storage)
    assert before <= note.created_at <= datetime.now(UTC)
    assert note.created_at == note.updated_at


def test_append_preserves_old(storage):
    a = add_note("А", "Б", storage)
    b = add_note("В", "Г", storage)
    assert storage.load_all() == [a, b]


def test_invalid_keeps_old(storage):
    a = add_note("А", "Б", storage)
    with pytest.raises(ValidationError):
        add_note("", "Б", storage)
    assert storage.load_all() == [a]


def test_write_failure_preserves_old(storage):
    old = add_note("А", "Б", storage)
    with patch.object(storage, "save_all", side_effect=StorageError("Ошибка записи")):
        with pytest.raises(StorageError):
            add_note("В", "Г", storage)
    assert storage.load_all() == [old]


def test_read_error_propagated(storage):
    with patch.object(storage, "load_all", side_effect=StorageError("Ошибка чтения")):
        with pytest.raises(StorageError):
            add_note("А", "Б", storage)


def test_validation_functions(storage):
    assert validate_title(" А ") == "А"
    assert validate_body(" Б ") == "Б"
