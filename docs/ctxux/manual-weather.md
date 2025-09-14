# Contextual UX: manual-weather

Ручной ввод погоды

Экран ручного ввода метеоданных при оффлайне или отказе провайдера.

## Local Principles
- **minimal-required-input — Минимум обязательного ввода**
  - Rationale: Просим только критичные поля и даём разумные значения по умолчанию.
  - Acceptance:
    - Все поля подписаны и доступны в VoiceOver
    - Сохранение возможно при заполнении минимального набора
  - Telemetry:
    - `manual_weather_input`
  - Global: minimize-required-input, offline-first-graceful-fallback
  - Stories: us-12

## Refs
- **UserStory**:
  - us-12
- **GlobalPrinciple**:
  - minimize-required-input
  - offline-first-graceful-fallback
- **UserFlow**:
  - manual-weather
  - check-network-for-weather
  - fetch-weather

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/06_ctxux/screens/manual-weather.json