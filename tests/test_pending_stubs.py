"""Проверка промежуточных заглушек; не является реализацией сценариев."""

import pytest

from src.scenarios.delete_note import delete_note
from src.scenarios.edit_note import edit_note


@pytest.mark.parametrize(
    "fn,args",
    [
        (edit_note, ("a",)),
        (delete_note, ("a",)),
    ],
)
def test_pending_stub(fn, args, storage):
    with pytest.raises(NotImplementedError):
        fn(*args, storage)
