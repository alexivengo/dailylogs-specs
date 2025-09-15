
# Flow Node: documents-view <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.1.0</span>
  <span class="badge build">2025-09-15T10:16:00Z · <a href="https://github.com/alexivengo/dailylogs-specs/commits/main" target="_blank" rel="noopener" class="sha">8e5537c</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>

✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/

## Related
CtxUX:
<span class="chip">[documents-view](../../ctxux/documents-view.md)</span>
## Description
Type: `screen`

Список документов проекта с поиском и офлайн-кэшем (provisional).

## Inputs
- `project_id`


## Outgoing Edges
- **e-docs-back** — action: `back` → target: `project-dashboard`

## Analytics
- `documents_search`

## Refs
- PRD:#4_3
- PRD:#5
- PRD:#8
- CJM:#retention-advocacy

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/