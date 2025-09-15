# User Story: us-2 <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.0.0</span>
  <span class="badge build">2025-09-15T11:48:21Z · <a href="https://github.com/alexivengo/dailylogs-specs/commit/fb31dd8" target="_blank" rel="noopener" class="sha">fb31dd8</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>

✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/04_userstories/us/us-2.json
## Related
<p>
  <span class="chip"><a href="../stories/index.md#?flow=project-create,projects-empty">Flow nodes (2)</a></span>
</p>
Flow nodes:
<span class="chip">[`project-create`](../flow/nodes/project-create.md)</span><span class="chip">[`projects-empty`](../flow/nodes/projects-empty.md)</span>HIG: <span class="chip"><a href="../hig/us-2.md">кандидаты</a></span>

**Role:** новый пользователь  
**Capability:** ясный CTA на пустом экране проектов  
**Value:** сразу понять, как начать  
**Priority:** high  
**Status:** proposed

## Acceptance Criteria
- Given нет проектов When открываю приложение Then вижу пустое состояние с пояснением и CTA (FLOW:#projects-empty; PRD:#7)
- Given пустой экран When нажимаю CTA Then открывается форма создания (FLOW:#project-create; PRD:#4_1)
- Given VoiceOver When экран пуст Then объявляются: заголовок → подсказка → CTA; таргеты ≥44 pt (PRD:#10)

## Metrics
### Leading
- Empty State CTR (PRD:#11)### Lagging
- Onboarding Completion Rate (PRD:#11)
## Non-Functional Requirements
- **accessibility**: Контраст и поддержка Dynamic Type
- **localization**: Подсказки и CTA локализованы

## Refs
- PRD:#7
- PRD:#10
- PRD:#11
- CJM:#onboarding-first-project
- FLOW:#projects-empty
- FLOW:#project-create

## Analytics
- `empty_state_shown`
- `project_create_view`

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/04_userstories/us/us-2.json

<p class="page-meta">
  View in GitHub: <a href="https://github.com/alexivengo/dailylogs-specs/commit/fb31dd8" target="_blank" rel="noopener">@fb31dd8</a></p>