# Flow Node: day-entries-decision

Type: `decision`

Определяет, пустой ли день или уже содержит записи.

## Inputs
- `selected_date`


## Outgoing Edges
- **e-day-state-empty** — action: `proceed` → target: `day-log-empty` (guard: `entries_count == 0`)- **e-day-state-populated** — action: `proceed` → target: `day-log-populated` (guard: `entries_count > 0`)


## Refs
- PRD:#4_2
- CJM:#daily-logging

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/