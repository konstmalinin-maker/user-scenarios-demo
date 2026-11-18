"""SC-004: Редактирование заметки. FR-004, UR-004."""

from dataclasses import replace
from datetime import datetime, timezone

from src.domain.exceptions import NoteNotFoundError
from src.domain.note import Note
from src.domain.ports import INoteStorage
from src.scenarios.add_note import validate_body, validate_title


def edit_note(
    note_id: str, storage: INoteStorage, title: str | None = None, body: str | None = None
) -> Note:
    """SC-004: None сохраняет поле; пустая строка недопустима."""
    notes = storage.load_all()
    for index, note in enumerate(notes):
        if note.id == note_id:
            if title is None and body is None:
                return note
            updated = replace(
                note,
                title=note.title if title is None else validate_title(title),
                body=note.body if body is None else validate_body(body),
                updated_at=datetime.now(timezone.utc),
            )
            notes[index] = updated
            storage.save_all(notes)
            return updated
    raise NoteNotFoundError(f"Заметка {note_id} не найдена")
