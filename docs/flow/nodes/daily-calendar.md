
# Flow Node: daily-calendar <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.1.0</span>
  <span class="badge build">2025-09-15T11:28:52Z · <a href="https://github.com/alexivengo/dailylogs-specs/commits/main" target="_blank" rel="noopener" class="sha">a1a6d8b</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/
## Related
<p>
  <span class="chip">
    <a href="../stories/index.md#?flow=daily-calendar">Used in Stories (1)</a>
  </span>
</p>
Stories:
<span class="chip">[us-12](../../stories/us-12.md)</span>
## Description
Type: `screen`

Компактный календарь с индикаторами статуса дня и кнопкой «Сегодня».

## Inputs
- `project_id`

## Outputs
- `selected_date`
- `day_date`

## Outgoing Edges
- **e-cal-select-today** — action: `select_today` → target: `day-entries-decision`- **e-cal-future-date** — action: `select_date` → target: `future-date-error` (guard: `selected_date > today`)
## Errors
- `err-future-date` — Выбрана будущая дата. Действие заблокировано.

## Analytics
- `daily_calendar_view`

## Refs
- PRD:#4_2
- CJM:#daily-logging

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/

<p class="page-meta">
  View in GitHub: <a href="https://github.com/alexivengo/dailylogs-specs/commit/a1a6d8b" target="_blank" rel="noopener">@a1a6d8b</a></p>