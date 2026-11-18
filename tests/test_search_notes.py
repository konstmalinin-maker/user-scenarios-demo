"""SC-003: основной поток, альтернативы и ошибки сохранения."""

from unittest.mock import patch

import pytest

from src.domain.exceptions import StorageError, ValidationError
from src.scenarios.add_note import add_note
from src.scenarios.search_notes import search_notes


@pytest.mark.parametrize("query", ["", " ", "\n\t"])
def test_empty_query(storage, query):
    with pytest.raises(ValidationError, match="запрос"):
        search_notes(query, storage)


def test_title_casefold(storage):
    n = add_note("Покупки", "молоко", storage)
    assert search_notes("  ПОКУПКИ  ", storage) == [n]


def test_body_casefold(storage):
    n = add_note("А", "МОЛОКО", storage)
    assert search_notes("молок", storage) == [n]


def test_unicode_casefold(storage):
    n = add_note("Straße", "Б", storage)
    assert search_notes("STRASSE", storage) == [n]


def test_no_matches(storage):
    add_note("А", "Б", storage)
    assert search_notes("missing", storage) == []


def test_empty_storage(storage):
    assert search_notes("А", storage) == []


def test_sorted(storage):
    a = add_note("А", "Б", storage)
    b = add_note("А", "В", storage)
    assert search_notes("А", storage) == [b, a]


def test_no_write(storage):
    with patch.object(storage, "save_all") as save:
        search_notes("А", storage)
    save.assert_not_called()


def test_read_failure(storage):
    with patch.object(storage, "load_all", side_effect=StorageError("Ошибка чтения")):
        with pytest.raises(StorageError):
            search_notes("А", storage)


pytestmark = pytest.mark.scenario("SC-003")
