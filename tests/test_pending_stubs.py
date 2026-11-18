"""Промежуточный этап: проверяется именно NotImplementedError заглушки."""

import pytest

from src.scenarios.delete_note import delete_note
from src.scenarios.edit_note import edit_note
from src.scenarios.list_notes import list_notes
from src.scenarios.search_notes import search_notes


@pytest.mark.parametrize(
    "fn,args",
    [
        (list_notes, ()),
        (search_notes, ("А",)),
        (edit_note, ("unknown",)),
        (delete_note, ("unknown",)),
    ],
)
def test_pending_stub(fn, args, storage):
    with pytest.raises(NotImplementedError):
        fn(*args, storage)
