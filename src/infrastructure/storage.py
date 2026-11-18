"""JSON-адаптер; атомарная замена файла в пределах одной ФС."""
import json
import os
from pathlib import Path
import tempfile
from src.domain.exceptions import StorageError
from src.domain.note import Note
from src.domain.ports import INoteStorage

class NoteStorage(INoteStorage):
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def load_all(self) -> list[Note]:
        try:
            if not self.path.exists():
                return []
            data = json.loads(self.path.read_text(encoding="utf8"))
            if not isinstance(data, list):
                raise ValueError("Ожидался список заметок")
            notes = [Note.from_dict(item) for item in data]
            if len({n.id for n in notes}) != len(notes):
                raise ValueError("Повторный ID")
            return notes
        except (OSError, ValueError, TypeError, KeyError) as exc:
            raise StorageError(f"Ошибка чтения хранилища: {exc}") from exc

    def save_all(self, notes: list[Note]) -> None:
        tmp = None
        try:
            if len({n.id for n in notes}) != len(notes):
                raise ValueError("Повторный ID")
            fd, tmp = tempfile.mkstemp(dir=self.path.parent, suffix=".tmp")
            with os.fdopen(fd, "w", encoding="utf8") as stream:
                json.dump([n.to_dict() for n in notes], stream, ensure_ascii=False, indent=2)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(tmp, self.path)
        except (OSError, ValueError, TypeError) as exc:
            raise StorageError(f"Ошибка записи хранилища: {exc}") from exc
        finally:
            if tmp and os.path.exists(tmp):
                os.unlink(tmp)
