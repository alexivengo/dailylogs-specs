# User Story: us-1

**Role:** руководитель стройплощадки  
**Capability:** создать первый проект по минимальному набору полей  
**Value:** быстро начать работу и увидеть ценность  
**Priority:** high  
**Status:** proposed

## Acceptance Criteria
- Given пустой список проектов When нажимаю «Создать проект» Then открывается форма с обязательным «Название» (FLOW:#project-create; PRD:#4_1)
- Given форма валидна When жму «Сохранить» Then проект сохраняется офлайн и открывается дашборд (FLOW:#save-project; PRD:#8)
- Given первый запуск When пустое состояние Then вижу CTA и TipKit вместо блокирующего туториала (PRD:#7; CJM:#onboarding-first-project)

## Metrics
### Leading
- Time to First Project (PRD:#11)### Lagging
- Onboarding Completion Rate (PRD:#11)
## Non-Functional Requirements
- **performance**: Локальный save проекта ≤500 мс
- **security_privacy**: SwiftData, NSFileProtectionComplete
- **accessibility**: Корректные labels и порядок фокуса формы
- **localization**: Локализованные строки формы

## Refs
- PRD:#4_1
- PRD:#7
- PRD:#8
- PRD:#11
- CJM:#onboarding-first-project
- FLOW:#project-create
- FLOW:#save-project

## Analytics
- `project_create_view`
- `project_saved`
- `empty_state_shown`

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/04_userstories/us/us-1.json