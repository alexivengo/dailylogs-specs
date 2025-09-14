# Flow Node: error-save

Type: `error`

Сбой сохранения проекта (например, I/O/хранилище). Предложить повтор или отмену.

## Inputs
- `error_code`


## Outgoing Edges
- **e-save-retry** — action: `tap_retry` → target: `save-project`- **e-save-cancel** — action: `tap_cancel` → target: `cancel-out`

## Analytics
- `error_project_save`

## Refs
- PRD:#5
- PRD:#7
- CJM:#onboarding-first-project

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/