
# Flow Node: day-log-populated <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.1.0</span>
  <span class="badge build">2025-09-15T12:04:13Z · <a href="https://github.com/alexivengo/dailylogs-specs/commits/main" target="_blank" rel="noopener" class="sha">b310327</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/
## Related
<p>
  <span class="chip">
    <a href="../stories/index.md#?flow=day-log-populated">Used in Stories (0)</a>
  </span>
</p>

## Description
Type: `screen`

День с записями: список по группам, быстрые действия, переход к превью отчёта.

## Inputs
- `selected_date`
- `project_id`

## Outputs
- `day_date`

## Outgoing Edges
- **e-day-add-entry-populated** — action: `tap_add_entry` → target: `entry-editor`- **e-day-open-preview** — action: `open_report_preview` → target: `report-preview`- **e-weather-manage-populated** — action: `manage_weather` → target: `check-network-for-weather`

## Analytics
- `day_log_view`

## Refs
- PRD:#4_2
- PRD:#8
- CJM:#reporting-signoff

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/

<p class="page-meta">
  View in GitHub: <a href="https://github.com/alexivengo/dailylogs-specs/commit/b310327" target="_blank" rel="noopener">@b310327</a></p>