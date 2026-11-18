"""Сервис приложения: SC-001..SC-005; DIP через INoteStorage."""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone

from src.domain.exceptions import NoteNotFoundError, ValidationError
from src.domain.note import Note
from src.domain.ports import INoteStorage
from src.domain.validation import validate_body, validate_title


class NoteService:
    def __init__(self, storage: INoteStorage):
        self.storage = storage

    def add(self, title: str, body: str) -> Note:
        note = Note.new(validate_title(title), validate_body(body))
        self.storage.save_all([*self.storage.load_all(), note])
        return note

    def list(self) -> list[Note]:
        return sorted(self.storage.load_all(), key=lambda n: n.created_at, reverse=True)

    def search(self, query: str) -> list[Note]:
        query = query.strip().casefold()
        if not query:
            raise ValidationError("Поисковый запрос не может быть пустым")
        return [n for n in self.list() if query in n.title.casefold() or query in n.body.casefold()]

    def get(self, note_id: str) -> Note:
        for note in self.storage.load_all():
            if note.id == note_id:
                return note
        raise NoteNotFoundError(f"Заметка {note_id} не найдена")

    def edit(self, note_id: str, title: str | None = None, body: str | None = None) -> Note:
        notes = list(self.storage.load_all())
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
                self.storage.save_all(notes)
                return updated
        raise NoteNotFoundError(f"Заметка {note_id} не найдена")

    def delete(self, note_id: str) -> None:
        notes = list(self.storage.load_all())
        remaining = [n for n in notes if n.id != note_id]
        if len(remaining) == len(notes):
            raise NoteNotFoundError(f"Заметка {note_id} не найдена")
        self.storage.save_all(remaining)
