# Contextual UX: export-decision <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

Выбор формата экспорта

<p class="badges">
  <span class="badge version">v1.0.1</span>
  <span class="badge build">2025-09-15T10:16:01Z · <a href="https://github.com/alexivengo/dailylogs-specs/commit/8e5537c" target="_blank" rel="noopener" class="sha">8e5537c</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/06_ctxux/screens/export-decision.json

## Related
Flow nodes:
<span class="chip">[`export-decision`](../flow/nodes/export-decision.md)</span><span class="chip">[`export-generate`](../flow/nodes/export-generate.md)</span><span class="chip">[`report-preview-signed`](../flow/nodes/report-preview-signed.md)</span>Экран выбора формата и канала экспорта отчёта.

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