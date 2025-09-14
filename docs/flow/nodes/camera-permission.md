# Flow Node: camera-permission

Type: `decision`

Проверка статуса доступа к камере для съёмки фото.


## Outputs
- `permission_status`

## Outgoing Edges
- **e-cam-granted** — action: `granted` → target: `capture-photo` (guard: `permission_status == "granted"`)- **e-cam-denied** — action: `denied` → target: `camera-permission-error` (guard: `permission_status == "denied"`)

## Analytics
- `permission_check_camera`

## Refs
- PRD:#9
- CJM:#daily-logging

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/