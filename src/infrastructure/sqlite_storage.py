"""SQLite-адаптер того же INoteStorage; транзакционная замена снимка."""

import json
import sqlite3
from contextlib import closing
from pathlib import Path

from src.domain.exceptions import StorageError
from src.domain.note import Note
from src.domain.ports import INoteStorage

SCHEMA = "CREATE TABLE IF NOT EXISTS notes (id TEXT PRIMARY KEY, data TEXT NOT NULL)"


class SQLiteNoteStorage(INoteStorage):
    def __init__(self, path: str | Path):
        self.path = str(path)

    def load_all(self) -> list[Note]:
        try:
            with closing(sqlite3.connect(self.path)) as db, db:
                db.execute(SCHEMA)
                return [
                    Note.from_dict(json.loads(row[0]))
                    for row in db.execute("SELECT data FROM notes ORDER BY rowid")
                ]
        except (sqlite3.Error, ValueError, TypeError, KeyError) as exc:
            raise StorageError(f"Ошибка чтения SQLite: {exc}") from exc

    def save_all(self, notes: list[Note]) -> None:
        try:
            with closing(sqlite3.connect(self.path)) as db, db:
                db.execute(SCHEMA)
                db.execute("DELETE FROM notes")
                db.executemany(
                    "INSERT INTO notes (id, data) VALUES (?, ?)",
                    [(n.id, json.dumps(n.to_dict(), ensure_ascii=False)) for n in notes],
                )
        except (sqlite3.Error, ValueError, TypeError) as exc:
            raise StorageError(f"Ошибка записи SQLite: {exc}") from exc
