
# Flow Node: save-entry <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.1.0</span>
  <span class="badge build">2025-09-15T10:16:00Z · <a href="https://github.com/alexivengo/dailylogs-specs/commits/main" target="_blank" rel="noopener" class="sha">8e5537c</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>

✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/

## Related
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