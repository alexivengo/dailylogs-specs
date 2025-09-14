# Flow Node: app-launch

Type: `system`

Инициализация приложения, проверка локального стора (SwiftData), определение наличия проектов и статуса сети.


## Outputs
- `has_projects`
- `is_online`

## Outgoing Edges
- **e-app-start-to-empty** — action: `initiate` → target: `projects-empty` (guard: `has_projects == false`)

## Analytics
- `app_launch`

## Refs
- PRD:#5
- PRD:#7
- PRD:#8
- CJM:#onboarding-first-project

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/