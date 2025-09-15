
# Flow Node: export-error <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.1.0</span>
  <span class="badge build">2025-09-15T11:48:20Z · <a href="https://github.com/alexivengo/dailylogs-specs/commits/main" target="_blank" rel="noopener" class="sha">fb31dd8</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/
## Related
<p>
  <span class="chip">
    <a href="../stories/index.md#?flow=export-error">Used in Stories (2)</a>
  </span>
</p>
Stories:
<span class="chip">[us-10](../../stories/us-10.md)</span><span class="chip">[us-17](../../stories/us-17.md)</span>
## Description
Type: `error`

Ошибка при экспорте/шеринге (включая недостаток памяти).

## Inputs
- `error_code`

## Outputs
- `error_code`

## Outgoing Edges
- **e-export-retry** — action: `tap_retry` → target: `export-generate`- **e-export-abort** — action: `tap_cancel` → target: `report-preview-signed`

## Analytics
- `export_failed`

## Refs
- PRD:#9
- CJM:#reporting-signoff

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/

<p class="page-meta">
  View in GitHub: <a href="https://github.com/alexivengo/dailylogs-specs/commit/fb31dd8" target="_blank" rel="noopener">@fb31dd8</a></p>