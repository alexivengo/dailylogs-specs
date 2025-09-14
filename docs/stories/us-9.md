# User Story: us-9

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