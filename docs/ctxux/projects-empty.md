# Contextual UX: projects-empty <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

Пустой список проектов

<p class="badges">
  <span class="badge version">v1.0.1</span>
  <span class="badge build">2025-09-15T11:48:21Z · <a href="https://github.com/alexivengo/dailylogs-specs/commit/fb31dd8" target="_blank" rel="noopener" class="sha">fb31dd8</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/06_ctxux/screens/projects-empty.json
## Related
<p>
  <span class="chip"><a href="../flow/index.md#?ctxux=projects-empty">Flow (2)</a></span>
</p>
Flow nodes:
<span class="chip">[`project-create`](../flow/nodes/project-create.md)</span><span class="chip">[`projects-empty`](../flow/nodes/projects-empty.md)</span>Экран пустого списка с TipKit и CTA создания проекта.

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

<p class="page-meta">
  View in GitHub: <a href="https://github.com/alexivengo/dailylogs-specs/commit/fb31dd8" target="_blank" rel="noopener">@fb31dd8</a></p>