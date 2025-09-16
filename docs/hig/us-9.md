# HIG Patterns for us-9 <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.0.0</span>
  <span class="badge build">2025-09-15T12:04:14Z · <a href="https://github.com/alexivengo/dailylogs-specs/commit/b310327" target="_blank" rel="noopener" class="sha">b310327</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>

✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/05_hig/stories/us-9/candidates.json
предпросмотр отчёта и подписание с блокировкой дня

## Related
<p>
  <span class="chip"><a href="../stories/index.md#?flow=lock-day,report-preview,report-preview-signed,report-sign">Flow (4)</a></span>
</p>

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

<p class="page-meta">
  View in GitHub: <a href="https://github.com/alexivengo/dailylogs-specs/commit/b310327" target="_blank" rel="noopener">@b310327</a></p>