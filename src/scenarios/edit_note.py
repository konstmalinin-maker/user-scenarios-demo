"""SC-004: тонкая обёртка над NoteService; FR-004, UR-004."""

from src.domain.note import Note
from src.domain.ports import INoteStorage
from src.domain.service import NoteService


def edit_note(
    note_id: str, storage: INoteStorage, title: str | None = None, body: str | None = None
) -> Note:
    """Выполнить SC-004 с внедрённым хранилищем."""
    return NoteService(storage).edit(note_id, title, body)
