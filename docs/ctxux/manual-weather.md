# Contextual UX: manual-weather <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

Ручной ввод погоды

<p class="badges">
  <span class="badge version">v1.0.1</span>
  <span class="badge build">2025-09-15T10:16:01Z · <a href="https://github.com/alexivengo/dailylogs-specs/commit/8e5537c" target="_blank" rel="noopener" class="sha">8e5537c</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/06_ctxux/screens/manual-weather.json

## Related
Flow nodes:
<span class="chip">[`check-network-for-weather`](../flow/nodes/check-network-for-weather.md)</span><span class="chip">[`fetch-weather`](../flow/nodes/fetch-weather.md)</span><span class="chip">[`manual-weather`](../flow/nodes/manual-weather.md)</span>Экран ручного ввода метеоданных при оффлайне или отказе провайдера.

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