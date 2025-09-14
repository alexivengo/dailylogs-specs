# Flow Node: camera-permission-error

Type: `error`

Доступ к камере отклонён. Предложить открыть Настройки или продолжить без фото.



## Outgoing Edges
- **e-open-settings** — action: `open_settings` → target: `entry-editor`- **e-continue-without** — action: `continue_without_photo` → target: `entry-editor`

## Analytics
- `camera_permission_error_view`

## Refs
- PRD:#9
- CJM:#daily-logging

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/