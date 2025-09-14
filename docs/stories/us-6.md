# User Story: us-6

**Role:** руководитель стройплощадки  
**Capability:** прикреплять фото к записи  
**Value:** визуально документировать прогресс/проблемы  
**Priority:** medium  
**Status:** proposed

## Acceptance Criteria
- Given разрешение выдано When нажимаю «Прикрепить фото» Then открывается камера; после подтверждения фото прикрепляется (FLOW:#capture-photo; PRD:#4_2)
- Given фото прикреплено When просматриваю запись Then вижу миниатюру (FLOW:#entry-editor; PRD:#4_2)
- Given слабая сеть When синхронизирую Then сохраняется локально с флагом для аплоада (PRD:#8)

## Metrics
### Leading
- Photo attach rate (PRD:#11)### Lagging
- Time to Report (PRD:#11)
## Non-Functional Requirements
- **performance**: Прикрепление неблокирующее
- **security_privacy**: Запрашивать минимум прав
- **accessibility**: Озвучки кнопок камеры и подтверждения

## Refs
- PRD:#4_2
- PRD:#8
- PRD:#11
- FLOW:#entry-editor
- FLOW:#capture-photo

## Analytics
- `photo_captured`
- `entry_saved`

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/04_userstories/us/us-6.json