# Contextual UX: documents-view <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

Просмотр документов

<p class="badges">
  <span class="badge version">v1.0.1</span>
  <span class="badge build">2025-09-15T11:48:21Z · <a href="https://github.com/alexivengo/dailylogs-specs/commit/fb31dd8" target="_blank" rel="noopener" class="sha">fb31dd8</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/06_ctxux/screens/documents-view.json
## Related
<p>
  <span class="chip"><a href="../flow/index.md#?ctxux=documents-view">Flow (1)</a></span>
</p>
Flow nodes:
<span class="chip">[`documents-view`](../flow/nodes/documents-view.md)</span>Экран просмотра и поиска документов проекта с поддержкой фильтров и предпросмотра.

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

<p class="page-meta">
  View in GitHub: <a href="https://github.com/alexivengo/dailylogs-specs/commit/fb31dd8" target="_blank" rel="noopener">@fb31dd8</a></p>