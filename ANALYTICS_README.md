# Analytics Events — Documentation

This document defines the analytics events used by the product and the rules for adding new ones. The authoritative source of truth for event names and parameter types is `02_UserFlow_v1.json` (section `analytics_events`) together with `analytics_schema.json`.

## Governance
- Owners: Product + Analytics + Dev.
- Event names are immutable once shipped. Additive changes only.
- Parameters:
  - Prefer optional params; mark as `required: true` only when strictly necessary.
  - No PII.
  - Reuse Data Dictionary fields where applicable (see `02_UserFlow_v1.json.data_dictionary`).
- Review: Any new events/params require a PR updating:
  - `02_UserFlow_v1.json` (events/params and triggers)
  - `analytics_schema.json` (types and allowed values)
  - `IDs_LOCK.md` (stable IDs registry)
- CI: The validator checks event structure and param types against `analytics_schema.json`.

## Canonical Events (delta)
The following events were added in v1.1.0 and are considered stable:

### empty_state_cta_tapped
- When: user taps the primary CTA on the empty projects screen.
- Params:
  - `source_screen: string`
- Triggers: `projects-empty`, edge `e-empty-create`

### sheet_presented
- When: a modal sheet is presented (project-create, etc.).
- Params:
  - `sheet_name: string`
- Triggers: `project-create`

### project_save_retry
- When: retry is performed after a failed project save.
- Params:
  - `attempt: number`
  - `reason: "timeout" | "offline" | "server"`
- Triggers: node `error-save`, edge `e-save-retry`

### weather_fetch_fallback
- When: weather auto-fetch falls back to manual input.
- Params:
  - `reason: "timeout" | "offline" | "error"`
- Triggers: nodes `check-network-for-weather`, `manual-weather`

### documents_search
- When: user searches in the Documents Registry.
- Params:
  - `query_length: number`
  - `offline: boolean`
  - `results_count: number`
- Triggers: node `documents-view`

### gallery_bulk_attach
- When: user confirms bulk attach from Gallery.
- Params:
  - `count: number`
- Triggers: node `gallery`

## DD-driven Params (examples)
To improve traceability, several DD fields are included in event payloads where applicable.

- `day_date: string(ISO)` appears in:
  - `daily_calendar_view`, `day_log_view`, `entry_saved`, `report_signed`, `report_exported`, `weather_fetched`, `manual_weather_input`
- `entry_type: enum` appears in:
  - `entry_saved`
- Weather fields:
  - `weather_temp_c`, `weather_wind_ms`, `weather_precip_mm`, `weather_provider`, `weather_source` appear in:
    - `weather_fetched` (source = network)
    - `manual_weather_input` (source = manual; values optional, per user input)

## Payload Examples

```json
{
  "event": "entry_saved",
  "params": {
    "entry_id": "e-123",
    "source": "save_and_add_another",
    "day_date": "2025-09-14",
    "entry_type": "work"
  }
}
```

```json
{
  "event": "weather_fetched",
  "params": {
    "success": true,
    "provider": "open-meteo",
    "latency_ms": 420,
    "day_date": "2025-09-14",
    "weather_temp_c": 16.2,
    "weather_wind_ms": 3.1,
    "weather_precip_mm": 0.4,
    "weather_provider": "open-meteo",
    "weather_source": "network"
  }
}
```

```json
{
  "event": "manual_weather_input",
  "params": {
    "fields_filled": 2,
    "day_date": "2025-09-14",
    "weather_source": "manual",
    "weather_temp_c": 15
  }
}
```

## Adding a New Event (checklist)
- Define event name and rationale.
- Specify params: name, type, required, allowed_values (if enum), and description.
- Add triggers in `02_UserFlow_v1.json` near the relevant node/edge.
- Update `analytics_schema.json` with the new event and params.
- Update `IDs_LOCK.md`.
- Let CI (validator) run and ensure no issues.
