
# Flow Node: app-launch <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.1.0</span>
  <span class="badge build">2025-09-15T11:48:20Z · <a href="https://github.com/alexivengo/dailylogs-specs/commits/main" target="_blank" rel="noopener" class="sha">fb31dd8</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/
## Related
<p>
  <span class="chip">
    <a href="../stories/index.md#?flow=app-launch">Used in Stories (1)</a>
  </span>
</p>
Stories:
<span class="chip">[us-17](../../stories/us-17.md)</span>
## Description
Type: `system`

Инициализация приложения, проверка локального стора (SwiftData), определение наличия проектов и статуса сети.


## Outputs
- `has_projects`
- `is_online`

## Outgoing Edges
- **e-app-start-to-empty** — action: `initiate` → target: `projects-empty` (guard: `has_projects == false`)

## Analytics
- `app_launch`

## Refs
- PRD:#5
- PRD:#7
- PRD:#8
- CJM:#onboarding-first-project

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/

<p class="page-meta">
  View in GitHub: <a href="https://github.com/alexivengo/dailylogs-specs/commit/fb31dd8" target="_blank" rel="noopener">@fb31dd8</a></p>