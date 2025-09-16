
# Flow Node: report-preview-signed <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.1.0</span>
  <span class="badge build">2025-09-15T12:04:13Z · <a href="https://github.com/alexivengo/dailylogs-specs/commits/main" target="_blank" rel="noopener" class="sha">b310327</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/
## Related
<p>
  <span class="chip">
    <a href="../stories/index.md#?flow=report-preview-signed">Used in Stories (2)</a>
  </span>
</p>
Stories:
<span class="chip">[us-10](../../stories/us-10.md)</span><span class="chip">[us-9](../../stories/us-9.md)</span>CtxUX:
<span class="chip">[export-decision](../../ctxux/export-decision.md)</span>
## Description
Type: `screen`

Предпросмотр подписанного отчёта. Доступен быстрый экспорт.

## Inputs
- `signed_pdf_checksum`
- `selected_date`
- `project_id`


## Outgoing Edges
- **e-signed-export-pdf** — action: `open_export` → target: `export-decision`

## Analytics
- `report_preview_signed_view`

## Refs
- PRD:#9
- CJM:#reporting-signoff

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/

<p class="page-meta">
  View in GitHub: <a href="https://github.com/alexivengo/dailylogs-specs/commit/b310327" target="_blank" rel="noopener">@b310327</a></p>