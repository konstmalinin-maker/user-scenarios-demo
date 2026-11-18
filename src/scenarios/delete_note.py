"""SC-005: Удаление заметки. FR-005, UR-005."""

from src.domain.exceptions import NoteNotFoundError
from src.domain.ports import INoteStorage


def delete_note(note_id: str, storage: INoteStorage) -> None:
    """SC-005: удалить существующую заметку; подтверждение запрашивает CLI."""
    notes = storage.load_all()
    remaining = [n for n in notes if n.id != note_id]
    if len(remaining) == len(notes):
        raise NoteNotFoundError(f"Заметка {note_id} не найдена")
    storage.save_all(remaining)
