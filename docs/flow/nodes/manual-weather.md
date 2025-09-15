
# Flow Node: manual-weather <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.1.0</span>
  <span class="badge build">2025-09-15T11:28:52Z · <a href="https://github.com/alexivengo/dailylogs-specs/commits/main" target="_blank" rel="noopener" class="sha">a1a6d8b</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/
## Related
<p>
  <span class="chip">
    <a href="../stories/index.md#?flow=manual-weather">Used in Stories (1)</a>
  </span>
</p>
Stories:
<span class="chip">[us-5](../../stories/us-5.md)</span>CtxUX:
<span class="chip">[manual-weather](../../ctxux/manual-weather.md)</span>
## Description
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

<p class="page-meta">
  View in GitHub: <a href="https://github.com/alexivengo/dailylogs-specs/commit/a1a6d8b" target="_blank" rel="noopener">@a1a6d8b</a></p>