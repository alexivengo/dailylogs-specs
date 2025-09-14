# DailyLogs Specs

Моно-репозиторий продуктовой спецификации проекта DailyLogs: PRD, CJM, User Flow, UX-принципы, User Stories, HIG candidates и валидатор трассировки.

## Структура
- `specs/00_prd/` — PRD (разделы и индекс).
- `specs/01_cjm/` — CJM (стадии и индекс).
- `specs/02_userflow/` — User Flow (узлы, аналитика, словарь данных).
- `specs/03_ux_principles/` — Глобальные UX-принципы и реестры.
- `specs/04_userstories/` — User Stories (индекс и карточки us-*).
- `specs/05_hig/` — HIG pattern candidates (проекции из US).
- `specs/06_ctxux/` — Contextual UX (экраны с локальными принципами).
- `specs/_schemas/` — JSON Schema для модулей.
- `specs/_build/` — Скрипты сборки и артефакты монолитов.

## Требования
- Python 3.11+
- GitHub CLI (`gh`) для публикации/автоматизации (по желанию)
- macOS + Homebrew (опционально)

## Быстрый старт
Собрать монолиты и прогнать валидатор:

```bash
python3 specs/_build/build.py && python3 trace_validator.py
```

Артефакты сборки появляются в `specs/_build/`:
- `00_PRD_v1.json`
- `01_CJM_v1.json`
- `02_UserFlow_v1.json`
- `03_Global_UX_Principles_v1.json`
- `04_UserStories_v1.json`
- `05_HIG_Pattern_selection_v1.json`
- `06_Contextual_UX_Guidelines_v1.json`

## Локальный запуск SpecHub (портал)

Требуется: graphviz, Python venv.

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install mkdocs mkdocs-material jinja2 pydot graphviz markdownify
python3 specs/_build/build.py
python3 trace_validator.py
python3 docs/generate_docs.py
mkdocs serve
```

Откройте http://127.0.0.1:8000 — на главной будут обе диаграммы.

## Источники vs Артефакты

- Источники спецификаций: `specs/**`
- Артефакты монолитов: `specs/_build/*.json`
- Генерируемая документация: `docs/**`, диаграммы: `docs/_media/*.svg`

В страницах добавлены ссылки "✏️ Edit source" на соответствующие файлы под `specs/**`.

## Что проверяет валидатор
- Согласованность ссылок между PRD/CJM/UserFlow/UserStories/UX/CTXUX.
- Guard-выражения в рёбрах User Flow: только допустимые операторы, строковые литералы в кавычках.
- Data Dictionary coverage:
  - Все `required` ключи из `specs/02_userflow/data_dictionary.json` должны использоваться
    в `inputs`/`outputs`/`guards`.
  - `optional` ключи не генерируют предупреждения.
- CtxUX-трассировка:
  - `specs/06_ctxux/screens/*.json` → плоский `local_principles[]` в корне монолита.
  - Для каждого локального принципа ожидаются поля:
    - `id`, `title`, `screen_id` (добавляется сборкой), `telemetry`
    - `user_story_ids`: массив `us-*`
    - `global_principle_ids`: канонические ID из `03_ux_principles`
  - Валидатор строит карты покрытия:
    - "UserStory id → local principles"
    - "UX global principle id → local principles"

## Формат отчёта
- Информационные карты покрытия для PRD/CJM/UserFlow/UserStories/UX/CTXUX.
- Отдельный раздел "Data Dictionary coverage (required/optional)" с агрегатами.
- "✔ No issues found" — все проверки пройдены.

## Схемы
- Все схемы используют метасхему Draft-07 (IDE-дружественно):
  - пример: `specs/_schemas/ctxux_screen.schema.json` → `http://json-schema.org/draft-07/schema#`

## Добавление нового экрана CtxUX
1) Создать `specs/06_ctxux/screens/<screen-id>.json` по схеме:
```json
{
  "$schema": "../../_schemas/ctxux_screen.schema.json",
  "id": "projects-empty",
  "title": "Пустой список проектов",
  "desc": "Краткое описание",
  "local_principles": [
    {
      "id": "empty-to-create-primary",
      "title": "Название локального принципа",
      "rationale": "Почему это важно",
      "acceptance": ["Критерий 1", "Критерий 2"],
      "telemetry": ["event_name"],
      "global_principle_ids": ["one-screen-one-action"],
      "user_story_ids": ["us-10"]
    }
  ],
  "refs": {
    "UserStory": ["us-10"],
    "GlobalPrinciple": ["one-screen-one-action"],
    "UserFlow": ["projects-empty"]
  }
}
```
2) Запустить сборку и валидатор (см. выше).

## CI (рекомендации)
- В GitHub Actions (см. `.github/workflows/trace-validate.yml`) запускать:
  - `python3 specs/_build/build.py`
  - `python3 trace_validator.py`
- Блокировать PR при фатальных ошибках.

## Лицензия
Внутренние артефакты. Права принадлежат владельцу репозитория.
