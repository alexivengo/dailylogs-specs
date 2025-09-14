# Stable IDs Registry (IDs_LOCK)

Version: 2025-09-14
Owners:
- Product: approves routes and analytics naming
- Design: approves screen/edge semantics, accessibility
- Dev: maintains spec integrity and validator rules

Policy
- IDs are immutable once introduced. Never rename in-place.
- New IDs are additive. Deletions go through deprecation:
  - Mark as deprecated with rationale and sunset date.
  - Keep for at least one minor version with no functional use.
- Reviews required for any new IDs (see Owners table).

Owners matrix
- Nodes/Edges: Design + Product + Dev
- Analytics events: Product + Analytics + Dev

## Nodes (stable)
- app-launch
- projects-empty
- project-create
- project-dashboard
- daily-calendar
- day-log-empty
- day-log-populated
- entry-editor
- save-project
- save-entry
- report-preview
- report-sign
- report-preview-signed
- export-decision
- export-generate
- export-error
- success-done
- cancel-out
- camera-permission
- camera-permission-error
- capture-photo
- check-network-for-weather
- fetch-weather
- manual-weather
- lock-day
- future-date-error
- documents-view
- gallery

## Edges (key)
- e-empty-create
- e-create-submit
- e-save-proj-success
- e-entry-submit
- e-save-entry-success
- e-save-and-add-another
- e-day-open-preview
- e-preview-tap-sign
- e-lock-success
- e-export-format-pdf
- e-export-success
- e-export-error
- e-export-retry
- e-export-abort
- e-cam-denied
- e-cam-granted
- e-open-settings
- e-photo-success
- e-day-add-entry-empty
- e-day-add-entry-populated
- e-cal-select-today
- e-dash-open-daily
- e-dash-open-documents
- e-dash-open-gallery
- e-docs-back
- e-gallery-back

## Analytics Events (stable)
- app_launch
- empty_state_shown
- project_create_view
- project_create_attempt
- project_saved
- error_project_save
- project_dashboard_view
- daily_calendar_view
- open_today
- day_log_view
- tap_add_entry
- entry_editor_view
- entry_create_attempt
- entry_saved
- permission_check_camera
- camera_permission_error_view
- continue_without_photo
- open_settings_camera
- photo_captured
- weather_check
- weather_fetched
- manual_weather_input
- report_preview_view
- tap_sign
- report_signed
- report_preview_signed_view
- export_options_view
- export_process_started
- report_exported
- export_failed
- export_retry
- export_abort
- flow_success
- flow_cancel
- empty_state_cta_tapped
- sheet_presented
- project_save_retry
- weather_fetch_fallback
- documents_search
- gallery_bulk_attach


Review rules
- Propose new IDs in a PR updating this file, with owner approvals.
- Include: motivation, usage sites, and links to PRD/UX refs.
- Validator must pass before merge.
