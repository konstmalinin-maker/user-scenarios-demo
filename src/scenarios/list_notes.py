"""SC-002: Загрузить заметки, отсортировать по created_at по убыванию.

Требования: FR-002, UR-002.
"""
from src.domain.note import Note
from src.domain.ports import INoteStorage

def list_notes(storage: INoteStorage) -> list[Note]:
    """Покрывает SC-002; см. docs/scenarios.md."""
    # TODO: Загрузить заметки, отсортировать по created_at по убыванию.
    raise NotImplementedError("SC-002: list_notes")
