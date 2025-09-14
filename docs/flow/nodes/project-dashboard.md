# Flow Node: project-dashboard

Type: `screen`

Дашборд проекта с быстрыми ссылками на модули. Основной CTA — Журнал работ.

## Inputs
- `project_id`


## Outgoing Edges
- **e-dash-open-daily** — action: `open_daily_logs` → target: `daily-calendar`- **e-dash-open-documents** — action: `open_documents` → target: `documents-view`- **e-dash-open-gallery** — action: `open_gallery` → target: `gallery`

## Analytics
- `project_dashboard_view`

## Refs
- PRD:#4_1
- PRD:#4_2
- CJM:#daily-logging

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/