# Flow Node: save-project

Type: `system`

Проверка и сохранение проекта в SwiftData; атомарное сохранение, контекст @MainActor.

## Inputs
- `project_data`

## Outputs
- `project_id`

## Outgoing Edges
- **e-save-proj-success** — action: `handle_success` → target: `project-dashboard`- **e-save-proj-failure** — action: `handle_error` → target: `error-save`

## Analytics
- `project_saved`

## Refs
- PRD:#4_1
- PRD:#5
- CJM:#onboarding-first-project

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/