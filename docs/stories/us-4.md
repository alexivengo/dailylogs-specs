# User Story: us-4

**Role:** руководитель стройплощадки  
**Capability:** «Сохранить и добавить ещё»  
**Value:** ускорить ввод повторяющихся записей  
**Priority:** high  
**Status:** proposed

## Acceptance Criteria
- Given редактор записи When жму «Сохранить и добавить ещё» Then запись сохраняется офлайн и открывается новый пустой редактор (FLOW:#entry-editor, FLOW:#save-entry; PRD:#4_2)
- Given включено предзаполнение When открывается новый редактор Then копируются [ASSUMPTION] тип работ/пакет; уникальные поля сбрасываются (PRD:#4_2)
- Given ошибка сохранения When диалог Then доступны «Повторить/Отмена», озвучки корректны (FLOW:#error-entry-save; PRD:#10)

## Metrics
### Leading
- Entry Addition Time (PRD:#11)### Lagging
- Доля дней с журналом (PRD:#11)
## Non-Functional Requirements
- **performance**: Локальный save ≤200 мс
- **accessibility**: Порядок фокуса и читабельные ярлыки
- **localization**: Ошибки и подсказки локализованы

## Refs
- PRD:#4_2
- PRD:#8
- PRD:#10
- PRD:#11
- CJM:#daily-logging
- FLOW:#entry-editor
- FLOW:#save-entry
- FLOW:#error-entry-save

## Analytics
- `entry_editor_view`
- `entry_saved`

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/04_userstories/us/us-4.json