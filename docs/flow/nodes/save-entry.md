# Flow Node: save-entry

Type: `system`

Сохранение записи в SwiftData. Валидация и одно атомарное сохранение на действие.

## Inputs
- `entry_data`

## Outputs
- `entry_id`
- `source`

## Outgoing Edges
- **e-save-entry-success** — action: `handle_success` → target: `day-log-populated`- **e-save-entry-validation** — action: `handle_validation_error` → target: `entry-editor`- **e-save-entry-system-error** — action: `handle_error` → target: `error-entry-save`

## Analytics
- `entry_saved`

## Refs
- PRD:#4_2
- PRD:#5
- CJM:#daily-logging

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/