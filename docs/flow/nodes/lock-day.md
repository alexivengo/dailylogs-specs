
# Flow Node: lock-day <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.1.0</span>
  <span class="badge build">2025-09-15T12:04:13Z · <a href="https://github.com/alexivengo/dailylogs-specs/commits/main" target="_blank" rel="noopener" class="sha">b310327</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/
## Related
<p>
  <span class="chip">
    <a href="../stories/index.md#?flow=lock-day">Used in Stories (2)</a>
  </span>
</p>
Stories:
<span class="chip">[us-17](../../stories/us-17.md)</span><span class="chip">[us-9](../../stories/us-9.md)</span>
## Description
Type: `system`

Финализация дня: вычисление checksum, установка статуса locked (read-only).

## Inputs
- `signature_blob`
- `selected_date`
- `project_id`

## Outputs
- `signed_pdf_checksum`
- `signed_at`

## Outgoing Edges
- **e-lock-success** — action: `handle_success` → target: `report-preview-signed`- **e-lock-failure** — action: `handle_error` → target: `report-preview`

## Analytics
- `report_signed`

## Refs
- PRD:#9
- CJM:#reporting-signoff

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/

<p class="page-meta">
  View in GitHub: <a href="https://github.com/alexivengo/dailylogs-specs/commit/b310327" target="_blank" rel="noopener">@b310327</a></p>