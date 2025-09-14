# Flow Node: check-network-for-weather

Type: `decision`

Проверка сети для автоматического снимка погоды либо переход к ручному вводу.



## Outgoing Edges
- **e-net-available** — action: `proceed` → target: `fetch-weather` (guard: `is_online == true`)- **e-net-offline** — action: `fallback` → target: `manual-weather` (guard: `is_online == false`)

## Analytics
- `weather_check`

## Refs
- PRD:#8
- CJM:#daily-logging

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/