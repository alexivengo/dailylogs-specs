# Flow Node: entry-editor

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