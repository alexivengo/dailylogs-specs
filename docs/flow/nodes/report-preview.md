
# Flow Node: report-preview <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.1.0</span>
  <span class="badge build">2025-09-15T10:16:00Z · <a href="https://github.com/alexivengo/dailylogs-specs/commits/main" target="_blank" rel="noopener" class="sha">8e5537c</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>

✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/

## Related
Stories:
<span class="chip">[us-17](../../stories/us-17.md)</span><span class="chip">[us-9](../../stories/us-9.md)</span>
## Description
Type: `screen`

Предпросмотр PDF/A-2u отчёта с чек-листом готовности. Подпись доступна из этого экрана.

## Inputs
- `selected_date`
- `project_id`

## Outputs
- `day_status`
- `report_preview`

## Outgoing Edges
- **e-preview-tap-sign** — action: `tap_sign` → target: `report-sign`

## Analytics
- `report_preview_view`

## Refs
- PRD:#9
- CJM:#reporting-signoff

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/