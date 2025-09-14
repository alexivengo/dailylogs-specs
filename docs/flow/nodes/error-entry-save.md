# Flow Node: error-entry-save

Type: `error`

Системная ошибка сохранения записи (I/O). Предложить повтор или отмену.

## Inputs
- `error_code`


## Outgoing Edges
- **e-entry-retry** — action: `tap_retry` → target: `save-entry`- **e-entry-cancel** — action: `tap_cancel` → target: `day-log-populated`

## Analytics
- `error_entry_save`

## Refs
- PRD:#5
- CJM:#daily-logging

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/