
# Flow Node: app-launch <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.1.0</span>
  <span class="badge build">2025-09-15T10:16:00Z · <a href="https://github.com/alexivengo/dailylogs-specs/commits/main" target="_blank" rel="noopener" class="sha">8e5537c</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>

✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/

## Related
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