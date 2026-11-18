"""SC-003: Отклонить пустой запрос, искать без учёта регистра в заголовке и теле.

Требования: FR-003, UR-003.
"""
from src.domain.note import Note
from src.domain.ports import INoteStorage

def search_notes(query: str, storage: INoteStorage) -> list[Note]:
    """Покрывает SC-003; см. docs/scenarios.md."""
    # TODO: Отклонить пустой запрос, искать без учёта регистра в заголовке и теле.
    raise NotImplementedError("SC-003: search_notes")
