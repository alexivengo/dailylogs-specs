# User Story: us-9 <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.0.0</span>
  <span class="badge build">2025-09-15T10:16:01Z · <a href="https://github.com/alexivengo/dailylogs-specs/commit/8e5537c" target="_blank" rel="noopener" class="sha">8e5537c</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>

✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/04_userstories/us/us-9.json

## Related
Flow nodes:
<span class="chip">[`lock-day`](../flow/nodes/lock-day.md)</span><span class="chip">[`report-preview`](../flow/nodes/report-preview.md)</span><span class="chip">[`report-preview-signed`](../flow/nodes/report-preview-signed.md)</span><span class="chip">[`report-sign`](../flow/nodes/report-sign.md)</span>HIG: <span class="chip"><a href="../hig/us-9.md">кандидаты</a></span>

**Role:** руководитель стройплощадки  
**Capability:** предпросмотр отчёта и подписание с блокировкой дня  
**Value:** получить неизменяемый комплаенс-артефакт  
**Priority:** high  
**Status:** proposed

## Acceptance Criteria
- Given есть записи When открываю «Предпросмотр» Then генерируется PDF/A-2u с чек-листом (FLOW:#report-preview; PRD:#9)
- Given подписываю When подтверждаю подпись Then день получает статус locked и checksum (FLOW:#report-sign, FLOW:#lock-day; PRD:#9)
- Given день locked When открываю календарь/список Then редактирование недоступно, виден индикатор «Подписан» (FLOW:#report-preview-signed; PRD:#9)
- Given VoiceOver When экран подписи активен Then фокус: canvas → Confirm (PRD:#10)

## Metrics
### Leading
- Доля дней с превью (PRD:#11)- Доля дней, дошедших до подписи (PRD:#11)### Lagging
- % подписанных дней (PRD:#11)- Time to Report (PRD:#11)
## Non-Functional Requirements
- **performance**: Блокировка ≤1 с
- **security_privacy**: Неизменяемость locked, checksum
- **accessibility**: Порядок фокуса и озвучки
- **localization**: Локализованные статусы/подписи

## Refs
- PRD:#9
- PRD:#10
- PRD:#11
- CJM:#reporting-signoff
- FLOW:#report-preview
- FLOW:#report-sign
- FLOW:#lock-day
- FLOW:#report-preview-signed

## Analytics
- `report_preview_view`
- `tap_sign`
- `report_signed`
- `report_preview_signed_view`

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/04_userstories/us/us-9.json