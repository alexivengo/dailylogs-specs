# User Story: us-5 <button class="copy-link" aria-label="Copy page link" onclick="window.spechubCopyLink && window.spechubCopyLink()">🔗 Copy link</button>

<p class="badges">
  <span class="badge version">v1.0.0</span>
  <span class="badge build">2025-09-15T10:16:01Z · <a href="https://github.com/alexivengo/dailylogs-specs/commit/8e5537c" target="_blank" rel="noopener" class="sha">8e5537c</a></span>
  <span class="badge schema unknown">Schema unknown</span>
</p>

✏️ Edit source: https://github.com/alexivengo/dailylogs-specs/blob/main/specs/04_userstories/us/us-5.json

## Related
Flow nodes:
<span class="chip">[`check-network-for-weather`](../flow/nodes/check-network-for-weather.md)</span><span class="chip">[`fetch-weather`](../flow/nodes/fetch-weather.md)</span><span class="chip">[`manual-weather`](../flow/nodes/manual-weather.md)</span>HIG: <span class="chip"><a href="../hig/us-5.md">кандидаты</a></span>

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