"""SC-003: Поиск заметок. FR-003, UR-003."""

from src.domain.exceptions import ValidationError
from src.domain.note import Note
from src.domain.ports import INoteStorage


def search_notes(query: str, storage: INoteStorage) -> list[Note]:
    """SC-003: поиск без учёта регистра по заголовку или телу."""
    query = query.strip().casefold()
    if not query:
        raise ValidationError("Поисковый запрос не может быть пустым")
    notes = [
        n for n in storage.load_all() if query in n.title.casefold() or query in n.body.casefold()
    ]
    return sorted(notes, key=lambda n: n.created_at, reverse=True)
