# Flow Node: report-preview-signed

Type: `screen`

Предпросмотр подписанного отчёта. Доступен быстрый экспорт.

## Inputs
- `signed_pdf_checksum`
- `selected_date`
- `project_id`


## Outgoing Edges
- **e-signed-export-pdf** — action: `open_export` → target: `export-decision`

## Analytics
- `report_preview_signed_view`

## Refs
- PRD:#9
- CJM:#reporting-signoff

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/