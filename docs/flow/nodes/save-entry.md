
# Flow Node: save-entry <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.1.0</span>
  <span class="badge build">2025-09-15T12:04:13Z · <a href="https://github.com/alexivengo/dailylogs-specs/commits/main" target="_blank" rel="noopener" class="sha">b310327</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/
## Related
<p>
  <span class="chip">
    <a href="../stories/index.md#?flow=save-entry">Used in Stories (2)</a>
  </span>
</p>
Stories:
<span class="chip">[us-4](../../stories/us-4.md)</span><span class="chip">[us-8](../../stories/us-8.md)</span>
## Description
Type: `system`

Сохранение записи в SwiftData. Валидация и одно атомарное сохранение на действие.

## Inputs
- `entry_data`

## Outputs
- `entry_id`
- `source`

## Outgoing Edges
- **e-save-entry-success** — action: `handle_success` → target: `day-log-populated`- **e-save-entry-validation** — action: `handle_validation_error` → target: `entry-editor`- **e-save-entry-system-error** — action: `handle_error` → target: `error-entry-save`

## Analytics
- `entry_saved`

## Refs
- PRD:#4_2
- PRD:#5
- CJM:#daily-logging

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/

<p class="page-meta">
  View in GitHub: <a href="https://github.com/alexivengo/dailylogs-specs/commit/b310327" target="_blank" rel="noopener">@b310327</a></p>