# HIG Patterns for us-1 <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.0.0</span>
  <span class="badge build">2025-09-15T11:28:53Z · <a href="https://github.com/alexivengo/dailylogs-specs/commit/a1a6d8b" target="_blank" rel="noopener" class="sha">a1a6d8b</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>

✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/05_hig/stories/us-1/candidates.json
создать первый проект по минимальному набору полей

**Role:** руководитель стройплощадки  
**Value:** быстро начать работу и увидеть ценность

## Candidates
### Present creation form in a sheet (`sheet-create`)
- Action: Open creation surface
- HIG sections:
  - Modal presentations > Sheets
- SwiftUI primitives:
  - `Sheet`
  - `Button`
- Pros:
  - Isolates short, single-step task
  - Preserves context; easy cancel
- Cons:
  - Gesture dismissal risk
- Accessibility notes:
  - Trap focus; provide explicit Cancel; large hit targets
- Common mistakes:
  - Non-dismissible sheet without cause
- Scores: fit 5, load 5, consistency 5, a11y 5, risk 4, total 24
- Refs:
  - PRD: 4_1, 7, 8, 11
  - CJM: onboarding-first-project
  - Flow: project-create, save-project
  - Story: us-1

### Navigation push to creation view (`nav-push-create`)
- Action: Open creation surface
- HIG sections:
  - Navigation > Navigation Bars & Stack
- SwiftUI primitives:
  - `NavigationStack`
  - `NavigationLink`
- Pros:
  - Clear forward progress & back affordance
- Cons:
  - Overkill for a single-step form
  - Stack churn
- Accessibility notes:
  - Clear title; obvious Cancel in toolbar
- Common mistakes:
  - Hiding Cancel; vague 'Done'
- Scores: fit 4, load 4, consistency 5, a11y 5, risk 4, total 22
- Refs:
  - PRD: 4_1, 7, 8, 11
  - CJM: onboarding-first-project
  - Flow: project-create, save-project
  - Story: us-1

### Form with single required TextField & Save (`form-minimal`)
- Action: Input & save minimal data
- HIG sections:
  - Controls > Forms
  - Controls > Text Fields
- SwiftUI primitives:
  - `Form`
  - `TextField`
  - `Toolbar .confirmationAction`
  - `Alert (on failure)`
- Pros:
  - Native validation; inline errors; minimal chrome
- Cons:
  - Can feel heavy if over-sectioned
- Accessibility notes:
  - Use labels (not placeholders); DT and VO friendly
- Common mistakes:
  - Placeholder-only labels
- Scores: fit 5, load 5, consistency 5, a11y 5, risk 5, total 25
- Refs:
  - PRD: 4_1, 7, 8, 11
  - CJM: onboarding-first-project
  - Flow: project-create, save-project
  - Story: us-1


## Recommendation
- Best fit: sheet-create, form-minimal
- Rationale: One screen, one action. Use a sheet with a minimal Form; Alert handles failure; state is preserved.
- Refs:
  - PRD: 4_1, 7, 8, 11
  - CJM: onboarding-first-project
  - Flow: project-create, save-project
  - Story: us-1
---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/05_hig/stories/us-1/candidates.json

<p class="page-meta">
  View in GitHub: <a href="https://github.com/alexivengo/dailylogs-specs/commit/a1a6d8b" target="_blank" rel="noopener">@a1a6d8b</a></p>