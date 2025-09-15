# Contextual UX: gallery <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

Галерея вложений

<p class="badges">
  <span class="badge version">v1.0.1</span>
  <span class="badge build">2025-09-15T10:16:01Z · <a href="https://github.com/alexivengo/dailylogs-specs/commit/8e5537c" target="_blank" rel="noopener" class="sha">8e5537c</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/06_ctxux/screens/gallery.json

## Related
Flow nodes:
<span class="chip">[`camera-permission`](../flow/nodes/camera-permission.md)</span><span class="chip">[`camera-permission-error`](../flow/nodes/camera-permission-error.md)</span><span class="chip">[`capture-photo`](../flow/nodes/capture-photo.md)</span><span class="chip">[`gallery`](../flow/nodes/gallery.md)</span>Экран просмотра и пакетного прикрепления фото к записям, с обработкой разрешений камеры.

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