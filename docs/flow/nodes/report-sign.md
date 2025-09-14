# Flow Node: report-sign

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