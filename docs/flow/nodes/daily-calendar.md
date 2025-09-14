# Flow Node: daily-calendar

Type: `screen`

Компактный календарь с индикаторами статуса дня и кнопкой «Сегодня».

## Inputs
- `project_id`

## Outputs
- `selected_date`
- `day_date`

## Outgoing Edges
- **e-cal-select-today** — action: `select_today` → target: `day-entries-decision`- **e-cal-future-date** — action: `select_date` → target: `future-date-error` (guard: `selected_date > today`)
## Errors
- `err-future-date` — Выбрана будущая дата. Действие заблокировано.

## Analytics
- `daily_calendar_view`

## Refs
- PRD:#4_2
- CJM:#daily-logging

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/