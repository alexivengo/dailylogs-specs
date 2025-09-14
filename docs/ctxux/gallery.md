# Contextual UX: gallery

Галерея вложений

Экран просмотра и пакетного прикрепления фото к записям, с обработкой разрешений камеры.

## Local Principles
- **fast-primary-action — Быстрое первичное действие**
  - Rationale: Основной CTA — быстрое прикрепление фотографий к текущему дню.
  - Acceptance:
    - Кнопка прикрепления доступна в первом фокусе
    - Пакетное выделение работает с озвучиванием количества выбранных элементов
  - Telemetry:
    - `gallery_bulk_attach`
    - `photo_captured`
  - Global: one-screen-one-action, offline-first-graceful-fallback
  - Stories: us-13

## Refs
- **UserStory**:
  - us-21
- **HIG**:
  - camera
  - photo-gallery
- **Wireframes**:
  - Figma:DL-Gallery-v3
- **DesignSystem**:
  - Grid
  - Toolbar
- **GlobalPrinciple**:
  - one-screen-one-action
  - offline-first-graceful-fallback
- **UserFlow**:
  - gallery
  - capture-photo
  - camera-permission
  - camera-permission-error

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/06_ctxux/screens/gallery.json