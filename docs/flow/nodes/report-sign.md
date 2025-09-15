
# Flow Node: report-sign <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.1.0</span>
  <span class="badge build">2025-09-15T10:16:00Z · <a href="https://github.com/alexivengo/dailylogs-specs/commits/main" target="_blank" rel="noopener" class="sha">8e5537c</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>

✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/

## Related
Stories:
<span class="chip">[us-15](../../stories/us-15.md)</span><span class="chip">[us-17](../../stories/us-17.md)</span><span class="chip">[us-9](../../stories/us-9.md)</span>
## Description
Type: `screen`

Экран подписи: полотно для росписи и подтверждение. Можно ввести ФИО [ASSUMPTION].

## Inputs
- `report_preview`

## Outputs
- `signature_blob`
- `signer_name`

## Outgoing Edges
- **e-sign-confirm** — action: `confirm_signature` → target: `lock-day`

## Analytics
- `tap_sign`

## Refs
- PRD:#9
- CJM:#reporting-signoff

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/