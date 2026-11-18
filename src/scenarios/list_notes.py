"""SC-002: тонкая обёртка над NoteService; FR-002, UR-002."""

from src.domain.note import Note
from src.domain.ports import INoteStorage
from src.domain.service import NoteService


def list_notes(storage: INoteStorage) -> list[Note]:
    """Выполнить SC-002 с внедрённым хранилищем."""
    return NoteService(storage).list()
