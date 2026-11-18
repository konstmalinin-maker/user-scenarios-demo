"""CLI (B): только ввод/вывод и вызовы сценариев; бизнес-правила в сервисе."""

import argparse
import sys

from src.domain.exceptions import DomainError, ValidationError
from src.domain.service import NoteService
from src.infrastructure.factory import create_storage
from src.scenarios.add_note import add_note
from src.scenarios.delete_note import delete_note
from src.scenarios.edit_note import edit_note
from src.scenarios.list_notes import list_notes
from src.scenarios.search_notes import search_notes


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="note", description="Локальные заметки: add/list/search/edit/delete"
    )
    commands = p.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add", help="Добавить заметку")
    add.add_argument("--title")
    add.add_argument("--body")
    commands.add_parser("list", help="Показать заметки")
    search = commands.add_parser("search", help="Поиск по заголовку и тексту")
    search.add_argument("--query", required=True)
    edit = commands.add_parser("edit", help="Изменить заметку")
    edit.add_argument("id")
    edit.add_argument("--title")
    edit.add_argument("--body")
    delete = commands.add_parser("delete", help="Удалить с подтверждением")
    delete.add_argument("id")
    return p


def display(notes, empty_message):
    if not notes:
        print(empty_message)
        return
    print("ID | Заголовок | Дата (UTC)")
    for n in notes:
        print(f"{n.id} | {n.title} | {n.created_at.isoformat()}")


def main(argv=None) -> int:
    args = parser().parse_args(argv)
    try:
        storage = create_storage()
        if args.command == "add":
            interactive = args.title is None or args.body is None
            title, body = args.title, args.body
            while True:
                title = input("Заголовок: ") if title is None else title
                body = input("Текст: ") if body is None else body
                try:
                    note = add_note(title, body, storage)
                    break
                except ValidationError as exc:
                    if not interactive:
                        raise
                    print(f"Ошибка: {exc}. Повторите ввод.", file=sys.stderr)
                    title, body = None, None
            print(f"Заметка добавлена: {note.id}")
        elif args.command == "list":
            display(list_notes(storage), "Заметок пока нет")
        elif args.command == "search":
            display(search_notes(args.query, storage), "Ничего не найдено")
        elif args.command == "edit":
            NoteService(storage).get(args.id)
            title, body = args.title, args.body
            if title is None and body is None:
                title = input("Новый заголовок (Enter — оставить): ") or None
                body = input("Новый текст (Enter — оставить): ") or None
            note = edit_note(args.id, storage, title, body)
            print(f"Заметка сохранена: {note.id}")
        elif args.command == "delete":
            NoteService(storage).get(args.id)
            if input("Удалить заметку? [да/нет]: ").strip().casefold() not in {"да", "yes"}:
                print("Удаление отменено")
                return 0
            delete_note(args.id, storage)
            print("Заметка удалена")
        return 0
    except EOFError:
        print("Операция отменена: ввод завершён")
        return 0
    except DomainError as exc:
        print(f"Ошибка: {exc}", file=sys.stderr)
        return 2


def entrypoint():
    raise SystemExit(main())


if __name__ == "__main__":
    entrypoint()
