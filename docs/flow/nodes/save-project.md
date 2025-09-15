
# Flow Node: save-project <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.1.0</span>
  <span class="badge build">2025-09-15T12:04:13Z · <a href="https://github.com/alexivengo/dailylogs-specs/commits/main" target="_blank" rel="noopener" class="sha">b310327</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/
## Related
<p>
  <span class="chip">
    <a href="../stories/index.md#?flow=save-project">Used in Stories (1)</a>
  </span>
</p>
Stories:
<span class="chip">[us-1](../../stories/us-1.md)</span>
## Description
Type: `system`

Проверка и сохранение проекта в SwiftData; атомарное сохранение, контекст @MainActor.

## Inputs
- `project_data`

## Outputs
- `project_id`

## Outgoing Edges
- **e-save-proj-success** — action: `handle_success` → target: `project-dashboard`- **e-save-proj-failure** — action: `handle_error` → target: `error-save`

## Analytics
- `project_saved`

## Refs
- PRD:#4_1
- PRD:#5
- CJM:#onboarding-first-project

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/

<p class="page-meta">
  View in GitHub: <a href="https://github.com/alexivengo/dailylogs-specs/commit/b310327" target="_blank" rel="noopener">@b310327</a></p>