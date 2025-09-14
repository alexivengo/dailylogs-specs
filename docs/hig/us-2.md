# HIG Patterns for us-2

ясный CTA на пустом экране проектов

**Role:** новый пользователь  
**Value:** сразу понять, как начать

## Candidates
### ContentUnavailableView + primary CTA (`content-unavailable-view`)
- Action: Display empty state CTA
- HIG sections:
  - Onboarding > Empty States
- SwiftUI primitives:
  - `ContentUnavailableView`
  - `Button`
  - `TipKit (optional)`
- Pros:
  - Semantic empty-state layout
  - Pairs cleanly with a single CTA
  - Good default VO grouping
- Cons:
  - Less brand flexibility
- Accessibility notes:
  - Ensure VO order: title → hint → CTA
  - Maintain 44pt targets and contrast
- Common mistakes:
  - Multiple primary CTAs
  - Verbose copy
- Scores: fit 5, load 5, consistency 5, a11y 5, risk 5, total 25
- Refs:
  - PRD: 7, 10, 11
  - CJM: onboarding-first-project
  - Flow: projects-empty, project-create
  - Story: us-2

### VStack + Text/Image + Button (`vstack-empty`)
- Action: Display empty state CTA
- HIG sections:
  - Layout & Organization
- SwiftUI primitives:
  - `VStack`
  - `Text`
  - `Image`
  - `Button`
- Pros:
  - Full control & easy theming
- Cons:
  - Manual a11y and spacing
  - Easy to overdo copy
- Accessibility notes:
  - Assign heading role; 44pt; clear labels
- Common mistakes:
  - Missing accessibilityLabel on image
- Scores: fit 5, load 4, consistency 4, a11y 4, risk 4, total 21
- Refs:
  - PRD: 7, 10, 11
  - CJM: onboarding-first-project
  - Flow: projects-empty, project-create
  - Story: us-2

### TipKit inline tip next to CTA (`tipkit-inline`)
- Action: Contextual education
- HIG sections:
  - Onboarding > Educating People
- SwiftUI primitives:
  - `TipKit`
- Pros:
  - Non-blocking guidance
  - Dismissible
- Cons:
  - iOS 17+
  - Tips may be ignored
- Accessibility notes:
  - Use polite live region; tip must be focusable
- Common mistakes:
  - Overusing tips → fatigue
- Scores: fit 4, load 4, consistency 5, a11y 5, risk 4, total 22
- Refs:
  - PRD: 7, 10, 11
  - CJM: onboarding-first-project
  - Flow: projects-empty, project-create
  - Story: us-2


## Recommendation
- Best fit: content-unavailable-view
- Rationale: Semantic native empty state with single primary CTA; TipKit optional for contextual nudge.
- Refs:
  - PRD: 7, 10, 11
  - CJM: onboarding-first-project
  - Flow: projects-empty, project-create
  - Story: us-2

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/05_hig/stories/us-2/candidates.json