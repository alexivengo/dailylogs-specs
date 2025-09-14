# Flow Node: capture-photo

Type: `system`

Запуск камеры, захват фото и сохранение офлайн. Автопривязка к черновику записи.


## Outputs
- `photo_id`

## Outgoing Edges
- **e-photo-success** — action: `handle_success` → target: `entry-editor`

## Analytics
- `photo_captured`

## Refs
- PRD:#4_4
- CJM:#daily-logging

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/