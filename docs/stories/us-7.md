# User Story: us-7

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