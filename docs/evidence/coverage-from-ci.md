# Покрытие сценариев

Автоматически: `python scripts/coverage_report.py` после pytest в CI.
Число тестов — выполненные parameterized cases; JSON и SQLite считаются отдельно.
F: Must ≥90%, остальные ≥70%; A повышает итоговый порог каждого модуля до 90%.

| SC | Модуль | Покрытие | Тестов | Порог F | Итоговый A+F |
|---|---|---:|---:|---:|---:|
| SC-001 | `src/scenarios/add_note.py` | 100.0% | 40 | 90% | 90% |
| SC-002 | `src/scenarios/list_notes.py` | 100.0% | 10 | 90% | 90% |
| SC-003 | `src/scenarios/search_notes.py` | 100.0% | 22 | 70% | 90% |
| SC-004 | `src/scenarios/edit_note.py` | 100.0% | 30 | 70% | 90% |
| SC-005 | `src/scenarios/delete_note.py` | 100.0% | 14 | 70% | 90% |

Бизнес-логика `NoteService`: 100.0%; отдельный порог ≥90%, чтобы метрики тонких обёрток не скрывали непокрытые правила.
