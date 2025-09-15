# HIG Patterns for us-5 <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.0.0</span>
  <span class="badge build">2025-09-15T11:28:53Z · <a href="https://github.com/alexivengo/dailylogs-specs/commit/a1a6d8b" target="_blank" rel="noopener" class="sha">a1a6d8b</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>

✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/05_hig/stories/us-5/candidates.json
автоподстановка погоды онлайн и ручной ввод офлайн

**Role:** руководитель стройплощадки  
**Value:** закрывать день без блокеров

## Candidates
### Task-driven fetch with inline ProgressView and timeout (`task-progress`)
- Action: Auto-fetch
- HIG sections:
  - Feedback > Progress Indicators
- SwiftUI primitives:
  - `Task`
  - `ProgressView`
  - `Text`
- Pros:
  - Non-blocking; visible status; timeout-friendly
- Cons:
  - Spinner fatigue if long
- Accessibility notes:
  - Announce start/timeout; role='status'
- Common mistakes:
  - No timeout → hang state
- Scores: fit 5, load 4, consistency 5, a11y 4, risk 4, total 22
- Refs:
  - PRD: 8, 11
  - CJM: 
  - Flow: check-network-for-weather, fetch-weather
  - Story: us-5

### Inline form when offline/timeout (`inline-weather-form`)
- Action: Fallback manual
- HIG sections:
  - Controls > Forms
  - Controls > Pickers
- SwiftUI primitives:
  - `Form`
  - `TextField`
  - `Picker`
- Pros:
  - Keeps user in flow; works offline
- Cons:
  - Unit localization & validation work
- Accessibility notes:
  - Use LabeledContent; numeric keyboards; avoid color-only cues
- Common mistakes:
  - Overpacked form
- Scores: fit 5, load 5, consistency 5, a11y 5, risk 4, total 24
- Refs:
  - PRD: 8, 11
  - CJM: 
  - Flow: manual-weather
  - Story: us-5


## Recommendation
- Best fit: task-progress, inline-weather-form
- Rationale: Do not block on network; inline fallback ensures closure.
- Refs:
  - PRD: 8, 11
  - CJM: 
  - Flow: check-network-for-weather, fetch-weather, manual-weather
  - Story: us-5
---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/05_hig/stories/us-5/candidates.json

<p class="page-meta">
  View in GitHub: <a href="https://github.com/alexivengo/dailylogs-specs/commit/a1a6d8b" target="_blank" rel="noopener">@a1a6d8b</a></p>