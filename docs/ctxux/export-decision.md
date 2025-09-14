# Contextual UX: export-decision

Выбор формата экспорта

Экран выбора формата и канала экспорта отчёта.

## Local Principles
- **clear-default-and-safe-cancel — Чёткий формат по умолчанию и безопасная отмена**
  - Rationale: По умолчанию предлагается совместимый формат PDF/A-2u, с явной возможностью отмены без потери данных.
  - Acceptance:
    - Формат по умолчанию видим и отмечен
    - Отмена возвращает на предыдущий экран без сайд-эффектов
  - Telemetry:
    - `export_options_view`
  - Global: one-screen-one-action, explicit-status-signature-locking
  - Stories: us-1, us-2

## Refs
- **UserStory**:
  - us-1
  - us-2
- **GlobalPrinciple**:
  - one-screen-one-action
  - explicit-status-signature-locking
- **UserFlow**:
  - export-decision
  - export-generate
  - report-preview-signed

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/06_ctxux/screens/export-decision.json