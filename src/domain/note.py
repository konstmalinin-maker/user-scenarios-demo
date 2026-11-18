"""Неизменяемая сущность заметки."""

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4


@dataclass(frozen=True)
class Note:
    id: str
    title: str
    body: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def new(cls, title: str, body: str) -> "Note":
        now = datetime.now(UTC)
        return cls(str(uuid4()), title, body, now, now)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Note":
        if (
            not isinstance(data, dict)
            or set(data) != {"id", "title", "body", "created_at", "updated_at"}
            or not all(isinstance(v, str) for v in data.values())
        ):
            raise ValueError("Некорректная запись заметки")
        created = datetime.fromisoformat(data["created_at"])
        updated = datetime.fromisoformat(data["updated_at"])
        if created.utcoffset() is None or updated.utcoffset() is None:
            raise ValueError("Дата должна содержать часовой пояс")
        return cls(data["id"], data["title"], data["body"], created, updated)
