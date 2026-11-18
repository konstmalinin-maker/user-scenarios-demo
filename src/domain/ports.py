"""DIP: сценарии зависят от порта, а не от формата хранения."""

from abc import ABC, abstractmethod

from src.domain.note import Note


class INoteStorage(ABC):
    @abstractmethod
    def load_all(self) -> list[Note]:
        """Прочитать снимок заметок; при ошибке StorageError."""

    @abstractmethod
    def save_all(self, notes: list[Note]) -> None:
        """Атомарно заменить снимок; при ошибке сохранить прежний."""
