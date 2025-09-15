
# Flow Node: camera-permission <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.1.0</span>
  <span class="badge build">2025-09-15T10:16:00Z · <a href="https://github.com/alexivengo/dailylogs-specs/commits/main" target="_blank" rel="noopener" class="sha">8e5537c</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>

✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/

## Related
CtxUX:
<span class="chip">[gallery](../../ctxux/gallery.md)</span>
## Description
Type: `decision`

Проверка статуса доступа к камере для съёмки фото.


## Outputs
- `permission_status`

## Outgoing Edges
- **e-cam-granted** — action: `granted` → target: `capture-photo` (guard: `permission_status == "granted"`)- **e-cam-denied** — action: `denied` → target: `camera-permission-error` (guard: `permission_status == "denied"`)

## Analytics
- `permission_check_camera`

## Refs
- PRD:#9
- CJM:#daily-logging

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/