
# Flow Node: entry-editor <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.1.0</span>
  <span class="badge build">2025-09-15T10:16:00Z · <a href="https://github.com/alexivengo/dailylogs-specs/commits/main" target="_blank" rel="noopener" class="sha">8e5537c</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>

✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/

## Related
Stories:
<span class="chip">[us-4](../../stories/us-4.md)</span><span class="chip">[us-6](../../stories/us-6.md)</span>
## Description
Type: `screen`

Форма записи: тип/интервалы/кол-во/заметки/вложения. Быстрые режимы: «Сохранить и добавить ещё», «Копировать из истории».

## Inputs
- `selected_date`

## Outputs
- `entry_data`
- `entry_type`

## Outgoing Edges
- **e-entry-attach-photo** — action: `attach_photo` → target: `camera-permission`- **e-entry-submit** — action: `tap_save_entry` → target: `save-entry`- **e-save-and-add-another** — action: `save_and_add_another` → target: `save-entry`
## Errors
- `err-entry-required` — Не заполнены обязательные поля записи.

## Analytics
- `entry_editor_view`

## Refs
- PRD:#4_2
- PRD:#4_4
- CJM:#daily-logging

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/