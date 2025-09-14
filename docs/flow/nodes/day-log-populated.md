# Flow Node: day-log-populated

Type: `screen`

День с записями: список по группам, быстрые действия, переход к превью отчёта.

## Inputs
- `selected_date`
- `project_id`

## Outputs
- `day_date`

## Outgoing Edges
- **e-day-add-entry-populated** — action: `tap_add_entry` → target: `entry-editor`- **e-day-open-preview** — action: `open_report_preview` → target: `report-preview`- **e-weather-manage-populated** — action: `manage_weather` → target: `check-network-for-weather`

## Analytics
- `day_log_view`

## Refs
- PRD:#4_2
- PRD:#8
- CJM:#reporting-signoff

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/