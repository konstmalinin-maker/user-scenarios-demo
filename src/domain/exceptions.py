"""Ошибки предметной области; интерфейс выводит их пользователю."""

class DomainError(Exception):
    """Базовая ошибка заметок."""

class ValidationError(DomainError):
    """Нарушено ограничение входных данных."""

class NoteNotFoundError(DomainError):
    """Заметка не найдена."""

class StorageError(DomainError):
    """Не удалось прочитать или сохранить данные."""
