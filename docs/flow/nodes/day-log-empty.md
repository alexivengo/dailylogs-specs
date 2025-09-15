
# Flow Node: day-log-empty <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.1.0</span>
  <span class="badge build">2025-09-15T11:48:20Z · <a href="https://github.com/alexivengo/dailylogs-specs/commits/main" target="_blank" rel="noopener" class="sha">fb31dd8</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/
## Related
<p>
  <span class="chip">
    <a href="../stories/index.md#?flow=day-log-empty">Used in Stories (0)</a>
  </span>
</p>

## Description
Type: `screen`

Пустой день: подсказки и CTA «Добавить запись», «Погода».

## Inputs
- `selected_date`
- `project_id`

## Outputs
- `day_date`

## Outgoing Edges
- **e-day-add-entry-empty** — action: `tap_add_entry` → target: `entry-editor`- **e-weather-manage-empty** — action: `manage_weather` → target: `check-network-for-weather`

## Analytics
- `day_log_view`

## Refs
- PRD:#4_2
- PRD:#8
- CJM:#daily-logging

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/

<p class="page-meta">
  View in GitHub: <a href="https://github.com/alexivengo/dailylogs-specs/commit/fb31dd8" target="_blank" rel="noopener">@fb31dd8</a></p>