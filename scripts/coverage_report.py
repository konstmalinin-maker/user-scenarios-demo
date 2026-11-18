"""F: метрики из coverage.json и фактически выполненных JUnit testcases."""

import json
import xml.etree.ElementTree as ET
from pathlib import Path

root = Path(__file__).resolve().parents[1]
data = json.loads((root / "coverage.json").read_text())
records = json.loads((root / "docs/scenarios.json").read_text())
cases = ET.parse(root / "junit.xml").findall(".//testcase")
rows = [
    "# Покрытие сценариев",
    "",
    "Автоматически: `python scripts/coverage_report.py` после pytest в CI.",
    "Число тестов — выполненные parameterized cases; JSON и SQLite считаются отдельно.",
    "F: Must ≥90%, остальные ≥70%; A повышает итоговый порог каждого модуля до 90%.",
    "",
    "| SC | Модуль | Покрытие | Тестов | Порог F | Итоговый A+F |",
    "|---|---|---:|---:|---:|---:|",
]
rtm = [
    "# Матрица трассируемости",
    "",
    "Обновляется после каждого merge; исходные требования и сценарии — docs/scenarios.md.",
    "",
    "| Сценарий | Требования | Модуль | Issue | Коммит реализации | Тест | Покрытие |",
    "|---|---|---|---|---|---|---:|",
]
failed = []
for r in records:
    cov = data["files"].get(r["module"], {}).get("summary", {}).get("percent_covered", 0)
    stem = Path(r["test"]).stem
    count = sum(c.get("classname", "").endswith(stem) for c in cases if c.find("skipped") is None)
    done = r["status"] == "implemented"
    if done and (cov < 90 or not count):
        failed.append(f"{r['id']}: coverage={cov:.1f}, tests={count}")
    rows.append(
        f"| {r['id']} | `{r['module']}` | {cov:.1f}% | {count} | {90 if r['priority'] == 'Must' else 70}% | {'90%' if done else 'заглушка'} |"
    )
    commit = r.get("implementation_commit", "в текущем PR" if done else "pr6-stubs")
    rtm.append(
        f"| {r['id']} | {', '.join(r['requirements'])} | `{r['module']}` | [#{r['issue']}](https://github.com/konstmalinin-maker/user-scenarios-demo/issues/{r['issue']}) | `{commit}` | `{r['test']}` | {f'{cov:.1f}%' if done else 'заглушка'} |"
    )
service = data["files"].get("src/domain/service.py")
if service:
    coverage = service["summary"]["percent_covered"]
    rows += [
        "",
        f"Бизнес-логика `NoteService`: {coverage:.1f}%; отдельный порог ≥90%, чтобы метрики тонких обёрток не скрывали непокрытые правила.",
    ]
    if coverage < 90:
        failed.append("NoteService <90%")
(root / "docs/coverage-report.md").write_text("\n".join(rows) + "\n", encoding="utf8")
(root / "docs/traceability.md").write_text("\n".join(rtm) + "\n", encoding="utf8")
print("\n".join(rows))
if failed:
    raise SystemExit("; ".join(failed))
