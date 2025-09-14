# HIG Patterns for us-5

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