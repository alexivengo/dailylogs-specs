# User Flow

| Узел | Тип | Исходящие | Аналитика | Refs |
|---|---|---:|---|---|
| [app-launch](nodes/app-launch.md) | system | 1 | app_launch | CJM: [onboarding-first-project](../cjm/onboarding-first-project.md) |
| [success-done](nodes/success-done.md) | terminator | 0 | flow_success | CJM: [reporting-signoff](../cjm/reporting-signoff.md) |
| [cancel-out](nodes/cancel-out.md) | terminator | 0 | flow_cancel | CJM: [daily-logging](../cjm/daily-logging.md) |
| [daily-calendar](nodes/daily-calendar.md) | screen | 2 | daily_calendar_view | CJM: [daily-logging](../cjm/daily-logging.md) |
| [day-entries-decision](nodes/day-entries-decision.md) | decision | 2 | — | CJM: [daily-logging](../cjm/daily-logging.md) |
| [day-log-empty](nodes/day-log-empty.md) | screen | 2 | day_log_view | CJM: [daily-logging](../cjm/daily-logging.md) |
| [day-log-populated](nodes/day-log-populated.md) | screen | 3 | day_log_view | CJM: [reporting-signoff](../cjm/reporting-signoff.md) |
| [documents-view](nodes/documents-view.md) | screen | 1 | documents_search | CJM: [retention-advocacy](../cjm/retention-advocacy.md) |
| [entry-editor](nodes/entry-editor.md) | screen | 3 | entry_editor_view | CJM: [daily-logging](../cjm/daily-logging.md) |
| [save-entry](nodes/save-entry.md) | system | 3 | entry_saved | CJM: [daily-logging](../cjm/daily-logging.md) |
| [error-entry-save](nodes/error-entry-save.md) | error | 2 | error_entry_save | CJM: [daily-logging](../cjm/daily-logging.md) |
| [report-preview](nodes/report-preview.md) | screen | 1 | report_preview_view | CJM: [reporting-signoff](../cjm/reporting-signoff.md) |
| [report-sign](nodes/report-sign.md) | screen | 1 | tap_sign | CJM: [reporting-signoff](../cjm/reporting-signoff.md) |
| [lock-day](nodes/lock-day.md) | system | 2 | report_signed | CJM: [reporting-signoff](../cjm/reporting-signoff.md) |
| [report-preview-signed](nodes/report-preview-signed.md) | screen | 1 | report_preview_signed_view | CJM: [reporting-signoff](../cjm/reporting-signoff.md) |
| [export-decision](nodes/export-decision.md) | decision | 3 | export_options_view | CJM: [reporting-signoff](../cjm/reporting-signoff.md) |
| [export-generate](nodes/export-generate.md) | system | 2 | export_process_started | CJM: [reporting-signoff](../cjm/reporting-signoff.md) |
| [export-error](nodes/export-error.md) | error | 2 | export_failed | CJM: [reporting-signoff](../cjm/reporting-signoff.md) |
| [camera-permission](nodes/camera-permission.md) | decision | 2 | permission_check_camera | CJM: [daily-logging](../cjm/daily-logging.md) |
| [capture-photo](nodes/capture-photo.md) | system | 1 | photo_captured | CJM: [daily-logging](../cjm/daily-logging.md) |
| [camera-permission-error](nodes/camera-permission-error.md) | error | 2 | camera_permission_error_view | CJM: [daily-logging](../cjm/daily-logging.md) |
| [gallery](nodes/gallery.md) | screen | 1 | gallery_bulk_attach | CJM: [daily-logging](../cjm/daily-logging.md) |
| [save-project](nodes/save-project.md) | system | 2 | project_saved | CJM: [onboarding-first-project](../cjm/onboarding-first-project.md) |
| [error-save](nodes/error-save.md) | error | 2 | error_project_save | CJM: [onboarding-first-project](../cjm/onboarding-first-project.md) |
| [future-date-error](nodes/future-date-error.md) | error | 0 | — | CJM: [daily-logging](../cjm/daily-logging.md) |
| [check-network-for-weather](nodes/check-network-for-weather.md) | decision | 2 | weather_check | CJM: [daily-logging](../cjm/daily-logging.md) |
| [projects-empty](nodes/projects-empty.md) | screen | 1 | empty_state_shown | CJM: [onboarding-first-project](../cjm/onboarding-first-project.md) |
| [project-create](nodes/project-create.md) | screen | 2 | project_create_view | CJM: [onboarding-first-project](../cjm/onboarding-first-project.md) |
| [project-dashboard](nodes/project-dashboard.md) | screen | 3 | project_dashboard_view | CJM: [daily-logging](../cjm/daily-logging.md) |
| [fetch-weather](nodes/fetch-weather.md) | system | 2 | weather_fetched | CJM: [daily-logging](../cjm/daily-logging.md) |
| [manual-weather](nodes/manual-weather.md) | screen | 1 | manual_weather_input | CJM: [daily-logging](../cjm/daily-logging.md) |
