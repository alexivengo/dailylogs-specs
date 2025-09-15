
# Flow Node: check-network-for-weather <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.1.0</span>
  <span class="badge build">2025-09-15T11:48:20Z · <a href="https://github.com/alexivengo/dailylogs-specs/commits/main" target="_blank" rel="noopener" class="sha">fb31dd8</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/
## Related
<p>
  <span class="chip">
    <a href="../stories/index.md#?flow=check-network-for-weather">Used in Stories (1)</a>
  </span>
</p>
Stories:
<span class="chip">[us-5](../../stories/us-5.md)</span>CtxUX:
<span class="chip">[manual-weather](../../ctxux/manual-weather.md)</span>
## Description
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

<p class="page-meta">
  View in GitHub: <a href="https://github.com/alexivengo/dailylogs-specs/commit/fb31dd8" target="_blank" rel="noopener">@fb31dd8</a></p>