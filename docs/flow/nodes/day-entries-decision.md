
# Flow Node: day-entries-decision <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.1.0</span>
  <span class="badge build">2025-09-15T12:04:13Z · <a href="https://github.com/alexivengo/dailylogs-specs/commits/main" target="_blank" rel="noopener" class="sha">b310327</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/
## Related
<p>
  <span class="chip">
    <a href="../stories/index.md#?flow=day-entries-decision">Used in Stories (0)</a>
  </span>
</p>

## Description
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

<p class="page-meta">
  View in GitHub: <a href="https://github.com/alexivengo/dailylogs-specs/commit/b310327" target="_blank" rel="noopener">@b310327</a></p>