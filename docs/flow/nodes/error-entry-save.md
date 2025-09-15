
# Flow Node: error-entry-save <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.1.0</span>
  <span class="badge build">2025-09-15T12:04:13Z · <a href="https://github.com/alexivengo/dailylogs-specs/commits/main" target="_blank" rel="noopener" class="sha">b310327</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/
## Related
<p>
  <span class="chip">
    <a href="../stories/index.md#?flow=error-entry-save">Used in Stories (2)</a>
  </span>
</p>
Stories:
<span class="chip">[us-15](../../stories/us-15.md)</span><span class="chip">[us-4](../../stories/us-4.md)</span>
## Description
Type: `error`

Системная ошибка сохранения записи (I/O). Предложить повтор или отмену.

## Inputs
- `error_code`


## Outgoing Edges
- **e-entry-retry** — action: `tap_retry` → target: `save-entry`- **e-entry-cancel** — action: `tap_cancel` → target: `day-log-populated`

## Analytics
- `error_entry_save`

## Refs
- PRD:#5
- CJM:#daily-logging

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/

<p class="page-meta">
  View in GitHub: <a href="https://github.com/alexivengo/dailylogs-specs/commit/b310327" target="_blank" rel="noopener">@b310327</a></p>