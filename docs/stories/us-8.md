# User Story: us-8 <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.0.0</span>
  <span class="badge build">2025-09-15T11:48:21Z · <a href="https://github.com/alexivengo/dailylogs-specs/commit/fb31dd8" target="_blank" rel="noopener" class="sha">fb31dd8</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>

✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/04_userstories/us/us-8.json
## Related
<p>
  <span class="chip"><a href="../stories/index.md#?flow=save-entry">Flow nodes (1)</a></span>
</p>
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

<p class="page-meta">
  View in GitHub: <a href="https://github.com/alexivengo/dailylogs-specs/commit/fb31dd8" target="_blank" rel="noopener">@fb31dd8</a></p>