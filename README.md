# Менеджер заметок — практическая работа №6

[![CI](https://github.com/konstmalinin-maker/user-scenarios-demo/actions/workflows/test.yml/badge.svg)](https://github.com/konstmalinin-maker/user-scenarios-demo/actions/workflows/test.yml)

**Малинин Константин Николаевич, М-25 ИО.** Пять сценариев: описание → Issue → заглушка → отдельный feature/PR → тесты → RTM. Основная часть и допзадания A–G. Python 3.12+, стандартная библиотека в runtime; MIT.

## Запуск

```bash
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip install -e .
note --help
```

Без установки команды `note` работает `python -m src.cli` с теми же аргументами.

```bash
note add --title "Покупки" --body "Молоко и хлеб"
note list
note search --query "МОЛОКО"
note edit ПОЛНЫЙ_UUID_ИЗ_LIST --title "Покупки на завтра"
note delete ПОЛНЫЙ_UUID_ИЗ_LIST
# Подтвердить: да / yes. Любой другой ответ или EOF отменяет удаление.
note add
# Интерактивный ввод; при ошибке валидации — повторный запрос.
note edit ПОЛНЫЙ_UUID_ИЗ_LIST
# Enter оставляет прежнее поле; --title "" является ошибкой.
```

По умолчанию `NOTES_BACKEND=json`, `NOTES_PATH=notes.json`. Для SQLite:

```bash
# Linux/macOS
export NOTES_BACKEND=sqlite
export NOTES_PATH=notes.sqlite3
note add --title "SQLite" --body "Тот же сценарий, другой адаптер"
note list
# Windows PowerShell:
# $env:NOTES_BACKEND="sqlite"
# $env:NOTES_PATH="notes.sqlite3"
```

Бэкенды используют разные файлы; переключение не переносит старые записи. Родительский каталог должен существовать. Программа рассчитана на одного владельца; параллельные записи не синхронизируются. Код возврата: 0 — успех/отмена, 2 — ошибка ввода/предметной области. Заголовок 1–100, тело 1–10000 после strip; пустой поиск — ошибка; полные UUID4, UTC-время.

## Проверка

```bash
ruff check .
python scripts/check_scenarios.py
python -m pytest -q --cov=src --cov-report=term-missing --cov-report=json --cov-report=xml --cov-report=html --cov-fail-under=80 --junitxml=junit.xml
python scripts/coverage_report.py
python scripts/demonstrate_checker.py
```

Все сценарные и CLI-тесты запускаются на JSON и SQLite. Автоматический отчёт в CI доступен в артефакте `scenario-metrics`; его генератор проверяет пороги A/F и покрытие бизнес-сервиса. Обязательная проверка ветки: `tests-and-scenarios`.

## Документы и история

[Отчёт по практике №6 с 21 скриншотом](PR6_Отчёт_Малинин.md).

- [Пять сценариев, основные и альтернативные потоки](docs/scenarios.md).
- [Матрица трассируемости](docs/traceability.md).
- [Покрытие по сценариям](docs/coverage-report.md).
- [Архитектура и DIP](docs/architecture.md).
- [Заглушки до реализации](https://github.com/konstmalinin-maker/user-scenarios-demo/tree/pr6-stubs).
- [Пять реализаций до рефакторинга C](https://github.com/konstmalinin-maker/user-scenarios-demo/tree/pr6-five-scenarios).
- PR реализации: [#6](https://github.com/konstmalinin-maker/user-scenarios-demo/pull/6), [#7](https://github.com/konstmalinin-maker/user-scenarios-demo/pull/7), [#8](https://github.com/konstmalinin-maker/user-scenarios-demo/pull/8), [#9](https://github.com/konstmalinin-maker/user-scenarios-demo/pull/9), [#10](https://github.com/konstmalinin-maker/user-scenarios-demo/pull/10).
