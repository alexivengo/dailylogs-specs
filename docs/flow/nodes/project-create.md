
# Flow Node: project-create <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.1.0</span>
  <span class="badge build">2025-09-15T11:48:20Z · <a href="https://github.com/alexivengo/dailylogs-specs/commits/main" target="_blank" rel="noopener" class="sha">fb31dd8</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/
## Related
<p>
  <span class="chip">
    <a href="../stories/index.md#?flow=project-create">Used in Stories (2)</a>
  </span>
</p>
Stories:
<span class="chip">[us-1](../../stories/us-1.md)</span><span class="chip">[us-2](../../stories/us-2.md)</span>CtxUX:
<span class="chip">[projects-empty](../../ctxux/projects-empty.md)</span>
## Description
Type: `screen`

Минимальная форма создания проекта: обязательное поле «Название проекта». Остальные поля — позже в дашборде.

## Inputs
- `project_name`

## Outputs
- `project_data`
- `project_name`

## Outgoing Edges
- **e-create-submit** — action: `submit_form` → target: `save-project` (guard: `len(project_name) > 0`)- **e-create-cancel** — action: `tap_cancel` → target: `cancel-out`
## Errors
- `err-project-name-required` — Пользователь нажал «Сохранить» без названия проекта.

## Analytics
- `project_create_view`

## Refs
- PRD:#4_1
- CJM:#onboarding-first-project

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/

<p class="page-meta">
  View in GitHub: <a href="https://github.com/alexivengo/dailylogs-specs/commit/fb31dd8" target="_blank" rel="noopener">@fb31dd8</a></p>