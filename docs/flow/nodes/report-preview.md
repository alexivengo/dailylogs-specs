# Flow Node: report-preview

Type: `screen`

Предпросмотр PDF/A-2u отчёта с чек-листом готовности. Подпись доступна из этого экрана.

## Inputs
- `selected_date`
- `project_id`

## Outputs
- `day_status`
- `report_preview`

## Outgoing Edges
- **e-preview-tap-sign** — action: `tap_sign` → target: `report-sign`

## Analytics
- `report_preview_view`

## Refs
- PRD:#9
- CJM:#reporting-signoff

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/