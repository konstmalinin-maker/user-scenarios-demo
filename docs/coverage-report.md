# Покрытие сценариев

Автоматически: `python scripts/coverage_report.py` после pytest в CI.
Число тестов — выполненные parameterized cases; JSON и SQLite считаются отдельно.
F: Must ≥90%, остальные ≥70%; A повышает итоговый порог каждого модуля до 90%.

| SC | Модуль | Покрытие | Тестов | Порог F | Итоговый A+F |
|---|---|---:|---:|---:|---:|
| SC-001 | `src/scenarios/add_note.py` | 100.0% | 20 | 90% | 90% |
| SC-002 | `src/scenarios/list_notes.py` | 100.0% | 5 | 90% | 90% |
| SC-003 | `src/scenarios/search_notes.py` | 100.0% | 11 | 70% | 90% |
| SC-004 | `src/scenarios/edit_note.py` | 100.0% | 0 | 70% | заглушка |
| SC-005 | `src/scenarios/delete_note.py` | 100.0% | 0 | 70% | заглушка |
