# Flow Node: fetch-weather

Type: `system`

Автозаполнение погоды через сеть (URLSession). В случае сбоя — остаётся ручной ввод.

## Inputs
- `selected_date`
- `project_location`

## Outputs
- `weather_data`
- `weather_temp_c`
- `weather_wind_ms`
- `weather_precip_mm`
- `weather_provider`
- `weather_source`

## Outgoing Edges
- **e-weather-success** — action: `handle_success` → target: `day-log-populated`- **e-weather-fail** — action: `handle_error` → target: `day-log-populated`

## Analytics
- `weather_fetched`

## Refs
- PRD:#8
- CJM:#daily-logging

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/