# Flow Node: export-decision

Type: `decision`

Выбор формата и канала экспорта: PDF/A-2u (по умолчанию) или другой формат; либо отмена.

## Inputs
- `signed_pdf_checksum`

## Outputs
- `export_format`
- `export_dest`

## Outgoing Edges
- **e-export-format-pdf** — action: `choose_pdf` → target: `export-generate` (guard: `export_format == "pdf_a_2u"`)- **e-export-format-other** — action: `choose_other_format` → target: `export-generate`- **e-export-cancel** — action: `tap_cancel` → target: `report-preview-signed`

## Analytics
- `export_options_view`

## Refs
- PRD:#4_2
- PRD:#9
- CJM:#reporting-signoff

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/