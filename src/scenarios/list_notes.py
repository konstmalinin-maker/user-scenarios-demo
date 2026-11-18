"""SC-002: Просмотр списка заметок. FR-002, UR-002."""

from src.domain.note import Note
from src.domain.ports import INoteStorage


def list_notes(storage: INoteStorage) -> list[Note]:
    """SC-002: новые заметки сверху; пустой список допустим."""
    return sorted(storage.load_all(), key=lambda n: n.created_at, reverse=True)
