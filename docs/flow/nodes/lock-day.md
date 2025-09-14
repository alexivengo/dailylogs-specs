# Flow Node: lock-day

Type: `system`

Финализация дня: вычисление checksum, установка статуса locked (read-only).

## Inputs
- `signature_blob`
- `selected_date`
- `project_id`

## Outputs
- `signed_pdf_checksum`
- `signed_at`

## Outgoing Edges
- **e-lock-success** — action: `handle_success` → target: `report-preview-signed`- **e-lock-failure** — action: `handle_error` → target: `report-preview`

## Analytics
- `report_signed`

## Refs
- PRD:#9
- CJM:#reporting-signoff

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/