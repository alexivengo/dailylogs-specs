# Flow Node: manual-weather

Type: `screen`

Экран ручного ввода погоды: температура, ветер, осадки. Данные сохраняются в день.


## Outputs
- `weather_manual`
- `weather_temp_c`
- `weather_wind_ms`
- `weather_precip_mm`
- `weather_source`

## Outgoing Edges
- **e-weather-submit** — action: `submit` → target: `day-log-populated`

## Analytics
- `manual_weather_input`

## Refs
- PRD:#4_2
- PRD:#8
- CJM:#daily-logging

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/