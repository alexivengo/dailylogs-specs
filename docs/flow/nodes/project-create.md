# Flow Node: project-create

Type: `screen`

Минимальная форма создания проекта: обязательное поле «Название проекта». Остальные поля — позже в дашборде.

## Inputs
- `project_name`

## Outputs
- `project_data`
- `project_name`

## Outgoing Edges
- **e-create-submit** — action: `submit_form` → target: `save-project` (guard: `len(project_name) > 0`)- **e-create-cancel** — action: `tap_cancel` → target: `cancel-out`
## Errors
- `err-project-name-required` — Пользователь нажал «Сохранить» без названия проекта.

## Analytics
- `project_create_view`

## Refs
- PRD:#4_1
- CJM:#onboarding-first-project

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/