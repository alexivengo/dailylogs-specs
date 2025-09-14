# Flow Node: export-generate

Type: `system`

Генерация файла выбранного формата и вызов iOS Share Sheet. Обработка таймаутов и low storage.

## Inputs
- `export_format`
- `selected_date`
- `project_id`

## Outputs
- `file_name`

## Outgoing Edges
- **e-export-success** — action: `handle_success` → target: `success-done`- **e-export-error** — action: `handle_error` → target: `export-error`

## Analytics
- `export_process_started`

## Refs
- PRD:#4_2
- PRD:#9
- CJM:#reporting-signoff

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/