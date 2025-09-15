# User Story: us-8 <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.0.0</span>
  <span class="badge build">2025-09-15T10:16:01Z · <a href="https://github.com/alexivengo/dailylogs-specs/commit/8e5537c" target="_blank" rel="noopener" class="sha">8e5537c</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>

✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/04_userstories/us/us-8.json

## Related
Flow nodes:
<span class="chip">[`save-entry`](../flow/nodes/save-entry.md)</span>
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