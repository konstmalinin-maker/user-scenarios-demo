"""SC-002: основной поток, альтернативы и ошибки сохранения."""

from dataclasses import replace
from datetime import timedelta
from unittest.mock import patch

import pytest

from src.domain.exceptions import StorageError
from src.scenarios.add_note import add_note
from src.scenarios.list_notes import list_notes


def test_empty(storage):
    assert list_notes(storage) == []


def test_single(storage):
    n = add_note("А", "Б", storage)
    assert list_notes(storage) == [n]


def test_newest_first(storage):
    old = add_note("Старое", "Б", storage)
    newer = replace(old, id="new", created_at=old.created_at + timedelta(days=1))
    storage.save_all([old, newer])
    assert list_notes(storage) == [newer, old]


def test_no_write(storage):
    with patch.object(storage, "save_all") as save:
        assert list_notes(storage) == []
    save.assert_not_called()


def test_read_failure(storage):
    with patch.object(storage, "load_all", side_effect=StorageError("Ошибка чтения")):
        with pytest.raises(StorageError):
            list_notes(storage)


pytestmark = pytest.mark.scenario("SC-002")
