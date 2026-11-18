"""SC-001: тонкая обёртка над NoteService; FR-001, UR-001."""

from src.domain.note import Note
from src.domain.ports import INoteStorage
from src.domain.service import NoteService
from src.domain.validation import validate_body as validate_body
from src.domain.validation import validate_title as validate_title


def add_note(title: str, body: str, storage: INoteStorage) -> Note:
    """Выполнить SC-001 с внедрённым хранилищем."""
    return NoteService(storage).add(title, body)
