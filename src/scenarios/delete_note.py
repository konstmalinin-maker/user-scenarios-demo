"""SC-005: Проверить существование ID, атомарно сохранить список без заметки.

Требования: FR-005, UR-005.
"""
from src.domain.ports import INoteStorage

def delete_note(note_id: str, storage: INoteStorage) -> None:
    """Покрывает SC-005; см. docs/scenarios.md."""
    # TODO: Проверить существование ID, атомарно сохранить список без заметки.
    raise NotImplementedError("SC-005: delete_note")
