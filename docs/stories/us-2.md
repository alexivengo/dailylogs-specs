# User Story: us-2

**Role:** новый пользователь  
**Capability:** ясный CTA на пустом экране проектов  
**Value:** сразу понять, как начать  
**Priority:** high  
**Status:** proposed

## Acceptance Criteria
- Given нет проектов When открываю приложение Then вижу пустое состояние с пояснением и CTA (FLOW:#projects-empty; PRD:#7)
- Given пустой экран When нажимаю CTA Then открывается форма создания (FLOW:#project-create; PRD:#4_1)
- Given VoiceOver When экран пуст Then объявляются: заголовок → подсказка → CTA; таргеты ≥44 pt (PRD:#10)

## Metrics
### Leading
- Empty State CTR (PRD:#11)### Lagging
- Onboarding Completion Rate (PRD:#11)
## Non-Functional Requirements
- **accessibility**: Контраст и поддержка Dynamic Type
- **localization**: Подсказки и CTA локализованы

## Refs
- PRD:#7
- PRD:#10
- PRD:#11
- CJM:#onboarding-first-project
- FLOW:#projects-empty
- FLOW:#project-create

## Analytics
- `empty_state_shown`
- `project_create_view`

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/04_userstories/us/us-2.json