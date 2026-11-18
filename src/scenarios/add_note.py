"""SC-001: Добавление заметки; FR-001, UR-001.

Проверить поля, создать UUID и время UTC, атомарно сохранить снимок.
При ошибке валидации или записи прежние данные остаются неизменными.
"""

from src.domain.exceptions import ValidationError
from src.domain.note import Note
from src.domain.ports import INoteStorage

TITLE_MAX = 100
BODY_MAX = 10_000


def validate_title(title: str) -> str:
    """SC-001: очищенный заголовок длиной 1..100."""
    title = title.strip()
    if not title:
        raise ValidationError("Заголовок не может быть пустым")
    if len(title) > TITLE_MAX:
        raise ValidationError("Заголовок не должен превышать 100 символов")
    return title


def validate_body(body: str) -> str:
    """SC-001: очищенное тело длиной 1..10000."""
    body = body.strip()
    if not body:
        raise ValidationError("Тело заметки не может быть пустым")
    if len(body) > BODY_MAX:
        raise ValidationError("Тело заметки не должно превышать 10000 символов")
    return body


def add_note(title: str, body: str, storage: INoteStorage) -> Note:
    """SC-001: сохранить новую заметку, вернуть её; ошибки DomainError."""
    note = Note.new(validate_title(title), validate_body(body))
    notes = storage.load_all()
    storage.save_all([*notes, note])
    return note
