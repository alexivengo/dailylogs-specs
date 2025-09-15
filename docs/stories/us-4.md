# User Story: us-4 <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.0.0</span>
  <span class="badge build">2025-09-15T11:48:21Z · <a href="https://github.com/alexivengo/dailylogs-specs/commit/fb31dd8" target="_blank" rel="noopener" class="sha">fb31dd8</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>

✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/04_userstories/us/us-4.json
## Related
<p>
  <span class="chip"><a href="../stories/index.md#?flow=entry-editor,error-entry-save,save-entry">Flow nodes (3)</a></span>
</p>
Flow nodes:
<span class="chip">[`entry-editor`](../flow/nodes/entry-editor.md)</span><span class="chip">[`error-entry-save`](../flow/nodes/error-entry-save.md)</span><span class="chip">[`save-entry`](../flow/nodes/save-entry.md)</span>HIG: <span class="chip"><a href="../hig/us-4.md">кандидаты</a></span>

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

<p class="page-meta">
  View in GitHub: <a href="https://github.com/alexivengo/dailylogs-specs/commit/fb31dd8" target="_blank" rel="noopener">@fb31dd8</a></p>