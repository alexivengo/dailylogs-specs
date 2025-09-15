
# Flow Node: error-save <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.1.0</span>
  <span class="badge build">2025-09-15T11:48:20Z · <a href="https://github.com/alexivengo/dailylogs-specs/commits/main" target="_blank" rel="noopener" class="sha">fb31dd8</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/
## Related
<p>
  <span class="chip">
    <a href="../stories/index.md#?flow=error-save">Used in Stories (1)</a>
  </span>
</p>
Stories:
<span class="chip">[us-18](../../stories/us-18.md)</span>
## Description
Type: `error`

Сбой сохранения проекта (например, I/O/хранилище). Предложить повтор или отмену.

## Inputs
- `error_code`


## Outgoing Edges
- **e-save-retry** — action: `tap_retry` → target: `save-project`- **e-save-cancel** — action: `tap_cancel` → target: `cancel-out`

## Analytics
- `error_project_save`

## Refs
- PRD:#5
- PRD:#7
- CJM:#onboarding-first-project

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/

<p class="page-meta">
  View in GitHub: <a href="https://github.com/alexivengo/dailylogs-specs/commit/fb31dd8" target="_blank" rel="noopener">@fb31dd8</a></p>