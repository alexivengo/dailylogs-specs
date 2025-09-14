# Flow Node: export-error

Type: `error`

Ошибка при экспорте/шеринге (включая недостаток памяти).

## Inputs
- `error_code`

## Outputs
- `error_code`

## Outgoing Edges
- **e-export-retry** — action: `tap_retry` → target: `export-generate`- **e-export-abort** — action: `tap_cancel` → target: `report-preview-signed`

## Analytics
- `export_failed`

## Refs
- PRD:#9
- CJM:#reporting-signoff

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/