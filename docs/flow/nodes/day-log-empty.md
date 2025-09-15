
# Flow Node: day-log-empty <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.1.0</span>
  <span class="badge build">2025-09-15T10:16:00Z · <a href="https://github.com/alexivengo/dailylogs-specs/commits/main" target="_blank" rel="noopener" class="sha">8e5537c</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>

✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/

## Related

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