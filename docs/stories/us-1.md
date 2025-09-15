# User Story: us-1 <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.0.0</span>
  <span class="badge build">2025-09-15T11:28:52Z · <a href="https://github.com/alexivengo/dailylogs-specs/commit/a1a6d8b" target="_blank" rel="noopener" class="sha">a1a6d8b</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>

✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/04_userstories/us/us-1.json
## Related
Flow nodes:
<span class="chip">[`project-create`](../flow/nodes/project-create.md)</span><span class="chip">[`save-project`](../flow/nodes/save-project.md)</span>HIG: <span class="chip"><a href="../hig/us-1.md">кандидаты</a></span>

**Role:** руководитель стройплощадки  
**Capability:** создать первый проект по минимальному набору полей  
**Value:** быстро начать работу и увидеть ценность  
**Priority:** high  
**Status:** proposed

## Acceptance Criteria
- Given пустой список проектов When нажимаю «Создать проект» Then открывается форма с обязательным «Название» (FLOW:#project-create; PRD:#4_1)
- Given форма валидна When жму «Сохранить» Then проект сохраняется офлайн и открывается дашборд (FLOW:#save-project; PRD:#8)
- Given первый запуск When пустое состояние Then вижу CTA и TipKit вместо блокирующего туториала (PRD:#7; CJM:#onboarding-first-project)

## Metrics
### Leading
- Time to First Project (PRD:#11)### Lagging
- Onboarding Completion Rate (PRD:#11)
## Non-Functional Requirements
- **performance**: Локальный save проекта ≤500 мс
- **security_privacy**: SwiftData, NSFileProtectionComplete
- **accessibility**: Корректные labels и порядок фокуса формы
- **localization**: Локализованные строки формы

## Refs
- PRD:#4_1
- PRD:#7
- PRD:#8
- PRD:#11
- CJM:#onboarding-first-project
- FLOW:#project-create
- FLOW:#save-project

## Analytics
- `project_create_view`
- `project_saved`
- `empty_state_shown`

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/04_userstories/us/us-1.json

<p class="page-meta">
  View in GitHub: <a href="https://github.com/alexivengo/dailylogs-specs/commit/a1a6d8b" target="_blank" rel="noopener">@a1a6d8b</a></p>