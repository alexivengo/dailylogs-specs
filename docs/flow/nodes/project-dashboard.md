
# Flow Node: project-dashboard <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.1.0</span>
  <span class="badge build">2025-09-15T10:16:01Z · <a href="https://github.com/alexivengo/dailylogs-specs/commits/main" target="_blank" rel="noopener" class="sha">8e5537c</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>

✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/

## Related

## Description
Type: `screen`

Дашборд проекта с быстрыми ссылками на модули. Основной CTA — Журнал работ.

## Inputs
- `project_id`


## Outgoing Edges
- **e-dash-open-daily** — action: `open_daily_logs` → target: `daily-calendar`- **e-dash-open-documents** — action: `open_documents` → target: `documents-view`- **e-dash-open-gallery** — action: `open_gallery` → target: `gallery`

## Analytics
- `project_dashboard_view`

## Refs
- PRD:#4_1
- PRD:#4_2
- CJM:#daily-logging

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/