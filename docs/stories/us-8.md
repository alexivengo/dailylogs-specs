# User Story: us-8

**Role:** руководитель стройплощадки  
**Capability:** копировать запись на другой день  
**Value:** ускорить ввод повторяющихся работ  
**Priority:** medium  
**Status:** proposed

## Acceptance Criteria
- Given список When выбираю «Копировать на другую дату» Then создаётся копия на выбранный день (PRD:#4_2)
- Given копирование When сохраняю Then операция атомарна, без перезаписи существующих (FLOW:#save-entry; PRD:#4_2)
- Given VoiceOver When завершено Then объявление «Запись скопирована» (PRD:#10)

## Metrics
### Leading
- Entry Addition Time (PRD:#11)### Lagging
- Доля дней с журналом (PRD:#11)
## Non-Functional Requirements
- **performance**: Операция локальная и быстрая
- **accessibility**: Подтверждающее объявление

## Refs
- PRD:#4_2
- PRD:#10
- PRD:#11
- FLOW:#save-entry

## Analytics
- `entry_copy_to_day`

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/04_userstories/us/us-8.json