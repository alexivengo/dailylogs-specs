# HIG Patterns for us-9

предпросмотр отчёта и подписание с блокировкой дня

**Role:** руководитель стройплощадки  
**Value:** неизменяемый комплаенс-артефакт

## Candidates
### PDFKit PDFView preview (`pdfkit-preview`)
- Action: Preview report
- HIG sections:
  - Content Views > Documents
- SwiftUI primitives:
  - `UIViewRepresentable(PDFView)`
- Pros:
  - Zoom/search/select; standard behavior
- Cons:
  - UIKit interop
- Accessibility notes:
  - Ensure text is VO-readable; buttons labeled
- Common mistakes:
  - Rendering as static bitmap
- Scores: fit 5, load 4, consistency 5, a11y 4, risk 5, total 23
- Refs:
  - PRD: 9, 11
  - CJM: reporting-signoff
  - Flow: report-preview
  - Story: us-9

### Signature canvas with Clear & Confirm (`canvas-signature`)
- Action: Capture signature
- HIG sections:
  - Controls > Custom drawing
- SwiftUI primitives:
  - `Canvas`
  - `Gesture`
  - `Button`
- Pros:
  - Natural signing; simple UI
- Cons:
  - Smoothing/export work
- Accessibility notes:
  - Label canvas; focus canvas→Confirm; include Clear
- Common mistakes:
  - Missing Clear/Undo; tiny targets
- Scores: fit 5, load 3, consistency 4, a11y 4, risk 4, total 20
- Refs:
  - PRD: 9, 11
  - CJM: reporting-signoff
  - Flow: report-sign
  - Story: us-9

### Alert with destructive 'Lock Day' (`alert-destructive-lock`)
- Action: Confirm lock
- HIG sections:
  - Feedback > Alerts
- SwiftUI primitives:
  - `Alert`
  - `Button(.destructive)`
- Pros:
  - Communicates finality; explicit decision
- Cons:
  - Limited to 2–3 actions
- Accessibility notes:
  - Use explicit titles; destructive role announces severity
- Common mistakes:
  - Ambiguous OK/Cancel
- Scores: fit 5, load 5, consistency 5, a11y 5, risk 5, total 25
- Refs:
  - PRD: 9, 11
  - CJM: reporting-signoff
  - Flow: lock-day, report-preview-signed
  - Story: us-9


## Recommendation
- Best fit: pdfkit-preview, alert-destructive-lock, canvas-signature
- Rationale: Strongest fidelity for preview; explicit confirmation for irreversible lock; custom canvas for signing.
- Refs:
  - PRD: 9, 11
  - CJM: reporting-signoff
  - Flow: report-preview, report-sign, lock-day, report-preview-signed
  - Story: us-9

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/05_hig/stories/us-9/candidates.json