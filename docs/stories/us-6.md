# User Story: us-6 <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.0.0</span>
  <span class="badge build">2025-09-15T10:16:01Z · <a href="https://github.com/alexivengo/dailylogs-specs/commit/8e5537c" target="_blank" rel="noopener" class="sha">8e5537c</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>

✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/04_userstories/us/us-6.json

## Related
Flow nodes:
<span class="chip">[`capture-photo`](../flow/nodes/capture-photo.md)</span><span class="chip">[`entry-editor`](../flow/nodes/entry-editor.md)</span>
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