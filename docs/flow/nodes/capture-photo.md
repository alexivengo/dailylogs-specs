
# Flow Node: capture-photo <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.1.0</span>
  <span class="badge build">2025-09-15T11:28:52Z · <a href="https://github.com/alexivengo/dailylogs-specs/commits/main" target="_blank" rel="noopener" class="sha">a1a6d8b</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/
## Related
<p>
  <span class="chip">
    <a href="../stories/index.md#?flow=capture-photo">Used in Stories (1)</a>
  </span>
</p>
Stories:
<span class="chip">[us-6](../../stories/us-6.md)</span>CtxUX:
<span class="chip">[gallery](../../ctxux/gallery.md)</span>
## Description
Type: `system`

Запуск камеры, захват фото и сохранение офлайн. Автопривязка к черновику записи.


## Outputs
- `photo_id`

## Outgoing Edges
- **e-photo-success** — action: `handle_success` → target: `entry-editor`

## Analytics
- `photo_captured`

## Refs
- PRD:#4_4
- CJM:#daily-logging

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/

<p class="page-meta">
  View in GitHub: <a href="https://github.com/alexivengo/dailylogs-specs/commit/a1a6d8b" target="_blank" rel="noopener">@a1a6d8b</a></p>