# Contextual UX: manual-weather <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

Ручной ввод погоды

<p class="badges">
  <span class="badge version">v1.0.1</span>
  <span class="badge build">2025-09-15T11:48:21Z · <a href="https://github.com/alexivengo/dailylogs-specs/commit/fb31dd8" target="_blank" rel="noopener" class="sha">fb31dd8</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/06_ctxux/screens/manual-weather.json
## Related
<p>
  <span class="chip"><a href="../flow/index.md#?ctxux=manual-weather">Flow (3)</a></span>
</p>
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

<p class="page-meta">
  View in GitHub: <a href="https://github.com/alexivengo/dailylogs-specs/commit/fb31dd8" target="_blank" rel="noopener">@fb31dd8</a></p>