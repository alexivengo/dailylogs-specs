
# Flow Node: camera-permission <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.1.0</span>
  <span class="badge build">2025-09-15T11:48:20Z · <a href="https://github.com/alexivengo/dailylogs-specs/commits/main" target="_blank" rel="noopener" class="sha">fb31dd8</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/
## Related
<p>
  <span class="chip">
    <a href="../stories/index.md#?flow=camera-permission">Used in Stories (0)</a>
  </span>
</p>
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

<p class="page-meta">
  View in GitHub: <a href="https://github.com/alexivengo/dailylogs-specs/commit/fb31dd8" target="_blank" rel="noopener">@fb31dd8</a></p>