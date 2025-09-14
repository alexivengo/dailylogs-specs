# Contextual UX: documents-view

Просмотр документов

Экран просмотра и поиска документов проекта с поддержкой фильтров и предпросмотра.

## Local Principles
- **progressive-disclosure — Последовательное раскрытие**
  - Rationale: Показывать минимум по умолчанию и раскрывать детали по требованию.
  - Acceptance:
    - Поиск доступен из одного фокуса
    - Фильтры применяются без перезагрузки экрана
  - Telemetry:
    - `documents_search`
  - Global: one-screen-one-action, minimize-required-input
  - Stories: us-13, us-14

## Refs
- **UserStory**:
  - us-13
  - us-14
- **HIG**:
  - search-bar
  - list-filtering
- **Wireframes**:
  - Figma:DL-Docs-View-v2
- **DesignSystem**:
  - List
  - SearchBar
- **GlobalPrinciple**:
  - one-screen-one-action
  - minimize-required-input
- **UserFlow**:
  - documents-view

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/06_ctxux/screens/documents-view.json