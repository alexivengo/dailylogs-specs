
# Flow Node: export-generate <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.1.0</span>
  <span class="badge build">2025-09-15T10:16:00Z · <a href="https://github.com/alexivengo/dailylogs-specs/commits/main" target="_blank" rel="noopener" class="sha">8e5537c</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>

✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/

## Related
Stories:
<span class="chip">[us-10](../../stories/us-10.md)</span><span class="chip">[us-11](../../stories/us-11.md)</span><span class="chip">[us-16](../../stories/us-16.md)</span><span class="chip">[us-17](../../stories/us-17.md)</span>CtxUX:
<span class="chip">[export-decision](../../ctxux/export-decision.md)</span>
## Description
Type: `system`

Генерация файла выбранного формата и вызов iOS Share Sheet. Обработка таймаутов и low storage.

## Inputs
- `export_format`
- `selected_date`
- `project_id`

## Outputs
- `file_name`

## Outgoing Edges
- **e-export-success** — action: `handle_success` → target: `success-done`- **e-export-error** — action: `handle_error` → target: `export-error`

## Analytics
- `export_process_started`

## Refs
- PRD:#4_2
- PRD:#9
- CJM:#reporting-signoff

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/02_userflow/nodes/