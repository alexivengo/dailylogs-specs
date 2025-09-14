# QA Checklist — A11y/UX for New Nodes

Scope: documents-view, gallery
Date: 2025-09-14
Owners: QA + Design

## Common Requirements (both screens)
- VoiceOver (VO)
  - Controls have accessibility labels and traits
  - VO focus order follows visual reading order
- Touch targets
  - All interactive elements have minimum size 44×44 pt
- Contrast
  - Text and essential UI provide contrast ratio ≥ 4.5:1 (WCAG AA)
- Dynamic Type
  - Large text does not truncate critical actions; content remains readable and tappable
- Reduce Motion / Reduce Transparency
  - Respect system settings without breaking task completion
- Spinners / Timeouts
  - No infinite spinners; operations have visible progress and clear fallback on timeout

---

## documents-view
- Screen basics
  - Title (or accessible label) announces entry to Documents Registry
  - Search field is labeled for VO; placeholder and hint are informative
- Focus navigation
  - VO Order: Title → Search → Filters (if any) → Results list → Footer/actions
  - Hardware keyboard tab order matches VO order
- Search behavior
  - Offline search returns cached results < 1s (set device to Airplane Mode)
  - Results count is announced or visible for VO users
  - Empty state provides guidance and primary next action
- List items
  - Each item exposes a clear label, secondary info, and an accessible action to open
  - Multi-line truncation does not hide critical identifiers
- Touch targets & contrast
  - Search, item actions, and top actions meet 44×44 and ≥4.5:1 contrast
- Motion/Transparency
  - Reduce Motion: transitions to results do not animate excessively
  - Reduce Transparency: backgrounds remain readable, controls remain discoverable
- Telemetry
  - documents_search fires with: query_length, offline, results_count

## gallery
- Screen basics
  - Title (or accessible label) announces entry to Gallery
  - Multi-select affordance is communicated to VO (trait/state)
- Focus navigation
  - VO Order: Title → Filter/Segmented controls → Grid items (row/col order) → Bulk actions
  - VO clearly announces selection state (selected/unselected) for items
- Selection persistence
  - Selection persists across pagination and filter changes
  - Returning to a prior page preserves selection state and focus does not jump unpredictably
- Bulk attach flow
  - Confirmation control is accessible and meets 44×44
  - After confirm, a success state is announced; errors include actionable recovery guidance
- Performance
  - Initial load and page changes avoid long spinners; fallback/empty states shown on timeout
- Motion/Transparency
  - Respect Reduce Motion/Transparency; no parallax or excessive blur when disabled
- Telemetry
  - gallery_bulk_attach fires with: count

## Test Data & Environments
- Offline mode: Airplane Mode; cached documents available
- VoiceOver: enabled; rotor navigation checks
- Display & Brightness: Text size set to larger accessibility sizes
- Accessibility settings: Reduce Motion ON, Reduce Transparency ON

## Exit Criteria
- All checks above passed for both screens
- No regressions introduced in existing flows
- Telemetry events visible in debug console/logs with expected parameters
