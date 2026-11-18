"""SC-003: тонкая обёртка над NoteService; FR-003, UR-003."""

from src.domain.note import Note
from src.domain.ports import INoteStorage
from src.domain.service import NoteService


def search_notes(query: str, storage: INoteStorage) -> list[Note]:
    """Выполнить SC-003 с внедрённым хранилищем."""
    return NoteService(storage).search(query)
