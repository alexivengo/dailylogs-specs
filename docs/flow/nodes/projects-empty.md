
# Flow Node: projects-empty <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.1.0</span>
  <span class="badge build">2025-09-15T10:16:01Z · <a href="https://github.com/alexivengo/dailylogs-specs/commits/main" target="_blank" rel="noopener" class="sha">8e5537c</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>

✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/

## Related
Stories:
<span class="chip">[us-2](../../stories/us-2.md)</span>CtxUX:
<span class="chip">[projects-empty](../../ctxux/projects-empty.md)</span>
## Description
Type: `screen`

Пустой список проектов с TipKit и CTA «Создать проект». Кратко объясняет следующий шаг.


## Outputs
- `project_location`

## Outgoing Edges
- **e-empty-create** — action: `tap_create_project` → target: `project-create`

## Analytics
- `empty_state_shown`

## Refs
- PRD:#4_1
- PRD:#7
- CJM:#onboarding-first-project

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/