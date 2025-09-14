# User Story: us-5

**Role:** руководитель стройплощадки  
**Capability:** автоподстановку погоды онлайн и ручной ввод офлайн  
**Value:** закрывать день без блокеров  
**Priority:** medium  
**Status:** proposed

## Acceptance Criteria
- Given сеть есть When открываю «Сегодня» Then погода подтягивается автоматически (FLOW:#fetch-weather; PRD:#8)
- Given офлайн/таймаут 8 с When не подтянулось Then переключаюсь на ручной ввод (FLOW:#manual-weather; PRD:#8)
- Given VoiceOver When редактирую погоду Then озвучиваются названия/единицы (PRD:#10)

## Metrics
### Leading
- Auto-weather share (PRD:#11)### Lagging
- Time to Report (PRD:#11)
## Non-Functional Requirements
- **performance**: Fetch погоды ≤8 с
- **accessibility**: Подписи полей/единиц измерения
- **localization**: Единицы/форматы по региону

## Refs
- PRD:#8
- PRD:#10
- PRD:#11
- CJM:#daily-logging
- FLOW:#check-network-for-weather
- FLOW:#fetch-weather
- FLOW:#manual-weather

## Analytics
- `weather_check`
- `weather_fetched`
- `manual_weather_input`

---
✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/04_userstories/us/us-5.json