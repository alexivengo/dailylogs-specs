# Changelog

All notable changes to this repository will be documented in this file.

## [1.1.0] - 2025-09-14
### Added
- `02_UserFlow_v1.json` bumped to `v1.1.0`.
- Added provisional nodes: `documents-view`, `gallery` (wired to `project-dashboard` with back edges), including CJM refs.
- Registered 6 analytics events and wired triggers:
  - `empty_state_cta_tapped`, `sheet_presented`, `project_save_retry`, `weather_fetch_fallback`, `documents_search`, `gallery_bulk_attach`.
- Enriched analytics params to include Data Dictionary fields:
  - `day_date` in `daily_calendar_view`, `day_log_view`, `entry_saved`, `report_signed`, `report_exported`, `weather_fetched`, `manual_weather_input`.
  - `entry_type` in `entry_saved`.
  - Weather metrics and provenance in weather events.
- `IDs_LOCK.md` created with policy, owners, and stable IDs registry.
- `analytics_schema.json` created; `trace_validator.py` updated to validate analytics and to treat analytics params as DD usage.
- `ANALYTICS_README.md` and `QA_CHECKLIST.md` added.

### Fixed
- Validator integration for `06_Contextual_UX_Guidelines_v1.json` cross-file checks, eliminating prior fatal issues.
 - Schemas: switched meta-schema to draft-07 (ctxux_screen.schema.json, hig_candidates.schema.json) to silence IDE warning about unsupported 2020-12 features.

### Notes
- CI: validator reports No issues found for this increment.

## [1.0.1] - 2025-09-14
### Changed
- `06_Contextual_UX_Guidelines_v1.json` bumped to `v1.0.1`.
- Mapped `global_principle_ids` to canonical ones.
- Adjusted meta context: split `export-flow` into `export-decision` and `export-generate`; `weather-inline` → `manual-weather`.

### Traceability snapshot
- New Flow nodes: `documents-view`, `gallery` (provisional) added to restore mapping for US-13/US-14.
- New analytics events registered and linked to nodes.
- Validator: 0 fatal, 0 warnings (DD warnings removed by wiring).

