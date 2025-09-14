# Contextual UX: projects-empty

Пустой список проектов

Экран пустого списка с TipKit и CTA создания проекта.

## Local Principles
- **empty-to-create-primary — Первичный CTA на пустом экране**
  - Rationale: Первичное действие на пустом экране должно быть максимально явным и доступным.
  - Acceptance:
    - Основной CTA фокусируем по Tab первым
    - Подсказка TipKit доступна для скринридера
  - Telemetry:
    - `empty_state_shown`
    - `empty_state_cta_tapped`
  - Global: one-screen-one-action, guide-and-request-in-the-moment
  - Stories: us-10

## Refs
- **UserStory**:
  - us-10
- **GlobalPrinciple**:
  - one-screen-one-action
  - guide-and-request-in-the-moment
- **UserFlow**:
  - projects-empty
  - project-create

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/06_ctxux/screens/projects-empty.json