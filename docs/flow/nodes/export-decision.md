
# Flow Node: export-decision <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.1.0</span>
  <span class="badge build">2025-09-15T12:04:13Z · <a href="https://github.com/alexivengo/dailylogs-specs/commits/main" target="_blank" rel="noopener" class="sha">b310327</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/
## Related
<p>
  <span class="chip">
    <a href="../stories/index.md#?flow=export-decision">Used in Stories (1)</a>
  </span>
</p>
Stories:
<span class="chip">[us-10](../../stories/us-10.md)</span>CtxUX:
<span class="chip">[export-decision](../../ctxux/export-decision.md)</span>
## Description
Type: `decision`

Выбор формата и канала экспорта: PDF/A-2u (по умолчанию) или другой формат; либо отмена.

## Inputs
- `signed_pdf_checksum`

## Outputs
- `export_format`
- `export_dest`

## Outgoing Edges
- **e-export-format-pdf** — action: `choose_pdf` → target: `export-generate` (guard: `export_format == "pdf_a_2u"`)- **e-export-format-other** — action: `choose_other_format` → target: `export-generate`- **e-export-cancel** — action: `tap_cancel` → target: `report-preview-signed`

## Analytics
- `export_options_view`

## Refs
- PRD:#4_2
- PRD:#9
- CJM:#reporting-signoff

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/

<p class="page-meta">
  View in GitHub: <a href="https://github.com/alexivengo/dailylogs-specs/commit/b310327" target="_blank" rel="noopener">@b310327</a></p>