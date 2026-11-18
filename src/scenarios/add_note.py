"""SC-001: Проверить поля, создать UUID, загрузить и атомарно сохранить заметку.

Требования: FR-001, UR-001.
"""
from src.domain.note import Note
from src.domain.ports import INoteStorage

def validate_title(title: str) -> str:
    """SC-001: валидация title."""
    # TODO: очистить пробелы, проверить длину 1..100.
    raise NotImplementedError("validate_title")

def validate_body(body: str) -> str:
    """SC-001: валидация body."""
    # TODO: очистить пробелы, проверить длину 1..10000.
    raise NotImplementedError("validate_body")

def add_note(title: str, body: str, storage: INoteStorage) -> Note:
    """Покрывает SC-001; см. docs/scenarios.md."""
    # TODO: Проверить поля, создать UUID, загрузить и атомарно сохранить заметку.
    raise NotImplementedError("SC-001: add_note")
