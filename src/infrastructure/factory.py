"""Выбор адаптера в точке сборки приложения, через окружение."""

import os

from src.domain.exceptions import ValidationError
from src.domain.ports import INoteStorage
from src.infrastructure.sqlite_storage import SQLiteNoteStorage
from src.infrastructure.storage import NoteStorage


def create_storage() -> INoteStorage:
    backend = os.environ.get("NOTES_BACKEND", "json").strip().lower()
    if backend == "json":
        return NoteStorage(os.environ.get("NOTES_PATH", "notes.json"))
    if backend == "sqlite":
        return SQLiteNoteStorage(os.environ.get("NOTES_PATH", "notes.sqlite3"))
    raise ValidationError("NOTES_BACKEND должен быть json или sqlite")
