
# Flow Node: fetch-weather <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.1.0</span>
  <span class="badge build">2025-09-15T12:04:13Z · <a href="https://github.com/alexivengo/dailylogs-specs/commits/main" target="_blank" rel="noopener" class="sha">b310327</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/
## Related
<p>
  <span class="chip">
    <a href="../stories/index.md#?flow=fetch-weather">Used in Stories (1)</a>
  </span>
</p>
Stories:
<span class="chip">[us-5](../../stories/us-5.md)</span>CtxUX:
<span class="chip">[manual-weather](../../ctxux/manual-weather.md)</span>
## Description
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

<p class="page-meta">
  View in GitHub: <a href="https://github.com/alexivengo/dailylogs-specs/commit/b310327" target="_blank" rel="noopener">@b310327</a></p>