# Flow Node: day-log-empty

Type: `screen`

Пустой день: подсказки и CTA «Добавить запись», «Погода».

## Inputs
- `selected_date`
- `project_id`

## Outputs
- `day_date`

## Outgoing Edges
- **e-day-add-entry-empty** — action: `tap_add_entry` → target: `entry-editor`- **e-weather-manage-empty** — action: `manage_weather` → target: `check-network-for-weather`

## Analytics
- `day_log_view`

## Refs
- PRD:#4_2
- PRD:#8
- CJM:#daily-logging

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/