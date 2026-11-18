"""Общие ограничения заголовка и тела (SC-001, SC-004)."""

from src.domain.exceptions import ValidationError

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
