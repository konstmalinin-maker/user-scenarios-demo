"""SC-005: тонкая обёртка над NoteService; FR-005, UR-005."""

from src.domain.ports import INoteStorage
from src.domain.service import NoteService


def delete_note(note_id: str, storage: INoteStorage) -> None:
    """Выполнить SC-005 с внедрённым хранилищем."""
    return NoteService(storage).delete(note_id)
