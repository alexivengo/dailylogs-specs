# User Story: us-7 <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.0.0</span>
  <span class="badge build">2025-09-15T11:28:53Z · <a href="https://github.com/alexivengo/dailylogs-specs/commit/a1a6d8b" target="_blank" rel="noopener" class="sha">a1a6d8b</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>

✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/04_userstories/us/us-7.json
## Related
Flow nodes:
<span class="chip">[`camera-permission-error`](../flow/nodes/camera-permission-error.md)</span>
**Role:** пользователь, ранее отклонивший доступ к камере  
**Capability:** инструкции и быстрый переход в Настройки для разблокировки фото  
**Value:** разблокировать фото  
**Priority:** medium  
**Status:** proposed

## Acceptance Criteria
- Given отказ камеры When пытаюсь прикрепить фото Then вижу диалог с «Открыть Настройки» / «Продолжить без фото» (FLOW:#camera-permission-error; PRD:#9)
- Given VoiceOver When открыт диалог Then корректные озвучки и фокус на сообщении (PRD:#10)

## Metrics
### Leading
- Permission Grant Rate (PRD:#11)### Lagging
- Доля дней с журналом (PRD:#11)
## Non-Functional Requirements
- **accessibility**: Alertdialog, live region, корректные ярлыки
- **localization**: Тексты/кнопки локализованы

## Refs
- PRD:#9
- PRD:#10
- PRD:#11
- FLOW:#camera-permission-error

## Analytics
- `camera_permission_error_view`
- `open_settings_camera`
- `continue_without_photo`

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/04_userstories/us/us-7.json

<p class="page-meta">
  View in GitHub: <a href="https://github.com/alexivengo/dailylogs-specs/commit/a1a6d8b" target="_blank" rel="noopener">@a1a6d8b</a></p>