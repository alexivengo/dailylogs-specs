# HIG Patterns for us-4 <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.0.0</span>
  <span class="badge build">2025-09-15T11:48:21Z · <a href="https://github.com/alexivengo/dailylogs-specs/commit/fb31dd8" target="_blank" rel="noopener" class="sha">fb31dd8</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>

✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/05_hig/stories/us-4/candidates.json
«Сохранить и добавить ещё»

## Related
<p>
  <span class="chip"><a href="../stories/index.md#?flow=entry-editor,error-entry-save,save-entry">Flow (3)</a></span>
</p>

**Role:** руководитель стройплощадки  
**Value:** ускорить ввод повторяющихся записей

## Candidates
### Form with explicit 'Save & Add Another' primary action (`form-save-add`)
- Action: Save and create new
- HIG sections:
  - Controls > Forms
  - Bars > Toolbars
- SwiftUI primitives:
  - `Form`
  - `Button`
  - `Toolbar .confirmationAction`
  - `FocusState`
- Pros:
  - Minimizes taps; predictable focus after reopen
  - Supports prefill policy
- Cons:
  - State management complexity
- Accessibility notes:
  - Announce success; autofocus first field
- Common mistakes:
  - Prefilling unique identifiers
- Scores: fit 5, load 5, consistency 5, a11y 5, risk 4, total 24
- Refs:
  - PRD: 4_2, 11
  - CJM: 
  - Flow: entry-editor, save-entry
  - Story: us-4

### Menu containing Save and Save & Add Another (`menu-save`)
- Action: Save and create new
- HIG sections:
  - Controls > Menus
  - Bars > Toolbars
- SwiftUI primitives:
  - `Menu`
  - `ToolbarItem`
- Pros:
  - Keeps toolbar uncluttered
- Cons:
  - Extra tap vs two primary buttons
- Accessibility notes:
  - Ensure menu labels read well in VO
- Common mistakes:
  - Hiding critical action in deep menu
- Scores: fit 4, load 4, consistency 5, a11y 5, risk 4, total 22
- Refs:
  - PRD: 4_2, 11
  - CJM: 
  - Flow: entry-editor, save-entry
  - Story: us-4

### Alert with Retry/Cancel on entry save failure (`alert-entry-retry`)
- Action: Errors
- HIG sections:
  - Feedback > Alerts
- SwiftUI primitives:
  - `Alert`
  - `ProgressView`
- Pros:
  - Consistent with project save error
- Cons:
  - Modal interruption
- Accessibility notes:
  - Assertive message; preserve state
- Common mistakes:
  - Vague messaging
- Scores: fit 5, load 5, consistency 5, a11y 5, risk 5, total 25
- Refs:
  - PRD: 10, 11
  - CJM: 
  - Flow: error-entry-save
  - Story: us-4


## Recommendation
- Best fit: form-save-add, alert-entry-retry
- Rationale: Fast loop for repetitive entry creation; reliable failure path.
- Refs:
  - PRD: 4_2, 10, 11
  - CJM: 
  - Flow: entry-editor, save-entry, error-entry-save
  - Story: us-4
---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/05_hig/stories/us-4/candidates.json

<p class="page-meta">
  View in GitHub: <a href="https://github.com/alexivengo/dailylogs-specs/commit/fb31dd8" target="_blank" rel="noopener">@fb31dd8</a></p>