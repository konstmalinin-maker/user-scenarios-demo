"""SC-004: Найти ID, проверить изменённые поля, сохранить с новым updated_at.

Требования: FR-004, UR-004.
"""

from src.domain.note import Note
from src.domain.ports import INoteStorage


def edit_note(
    note_id: str, storage: INoteStorage, title: str | None = None, body: str | None = None
) -> Note:
    """Покрывает SC-004; см. docs/scenarios.md."""
    # TODO: Найти ID, проверить изменённые поля, сохранить с новым updated_at.
    raise NotImplementedError("SC-004: edit_note")
