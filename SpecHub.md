отлично, запускаем «SpecHub». Ниже — подробное ТЗ для разработчика.

Цель

Собрать статический портал SpecHub поверх артефактов из specs/_build/*.json, чтобы:
	•	визуально просматривать связи PRD → CJM → User Flow → User Stories → HIG → Contextual UX;
	•	видеть диаграммы Flow/покрытия;
	•	быстро переходить к исходникам (модульным JSON) для правок;
	•	автоматически публиковать сайт (GitHub Pages) из CI.

Результат

Готовый репозиторий с:
	•	папкой /docs (сгенерированные MD + SVG/PNG диаграммы);
	•	генератором docs/generate_docs.py (из _build в Markdown + DOT→SVG);
	•	конфигом mkdocs.yml (тема Material, поиск, навигация);
	•	GitHub Action, который собирает и деплоит сайт на Pages;
	•	хук «Edit this page» → на модульные файлы в specs/**.

⸻

Исходные данные

Используем только артефакты после сборки:
	•	specs/_build/00_PRD_v1.json
	•	specs/_build/01_CJM_v1.json
	•	specs/_build/02_UserFlow_v1.json
	•	specs/_build/03_Global_UX_Principles_v1.json
	•	specs/_build/04_UserStories_v1.json
	•	specs/_build/05_HIG_Pattern_selection_v1.json
	•	specs/_build/06_Contextual_UX_Guidelines_v1.json

Также добавить экспорт:
	•	specs/_build/graph.json — единый граф связей (см. ниже структуру).

⸻

Технологический стек
	•	MkDocs + Material (статический сайт, поиск, оглавление, «Edit this page»).
	•	Python 3.10+: Jinja2, markdownify, pydot/graphviz, jsonschema (для sanity-check).
	•	Graphviz (dot → svg с кликабельными ссылками).
	•	GitHub Pages для публикации.

⸻

Новые директории/файлы

/docs
  /_media              # сгенерированные svg/png
  /_templates          # jinja-шаблоны
  index.md
  prd/*.md
  cjm/*.md
  flow/*.md
  stories/*.md
  ux/*.md
  hig/*.md
  ctxux/*.md
/docs/generate_docs.py
/mkdocs.yml
/.github/workflows/spechub.yml


⸻

Экспорт graph.json (добавить в build.py)

В конце сборки сформировать specs/_build/graph.json:

{
  "nodes": [
    {"id":"prd:4_2","type":"PRD","title":"..."},
    {"id":"cjm:daily-logging","type":"CJM","title":"..."},
    {"id":"flow:node:entry-editor","type":"FLOW_NODE","title":"Entry editor"},
    {"id":"flow:edge:entry-editor:e-entry-submit","type":"FLOW_EDGE","title":"..."},
    {"id":"story:us-12","type":"STORY","title":"..."},
    {"id":"hig:us-12:candidate:sheet","type":"HIG","title":"..."},
    {"id":"ux:principle:one-screen-one-action","type":"UX","title":"..."},
    {"id":"ctxux:screen:documents-view","type":"CTXUX","title":"..."},
    {"id":"analytics:event:entry_saved","type":"ANALYTICS","title":"..."},
    {"id":"dd:weather_temp_c","type":"DD","title":"..."}
  ],
  "edges": [
    {"from":"prd:4_2","to":"cjm:daily-logging","type":"influences"},
    {"from":"cjm:daily-logging","to":"flow:node:entry-editor","type":"maps_to"},
    {"from":"flow:node:entry-editor","to":"story:us-12","type":"covered_by"},
    {"from":"story:us-12","to":"hig:us-12:candidate:sheet","type":"selects"},
    {"from":"ux:principle:one-screen-one-action","to":"ctxux:screen:documents-view","type":"applies_to"},
    {"from":"flow:node:entry-editor","to":"analytics:event:entry_saved","type":"emits"},
    {"from":"dd:weather_temp_c","to":"flow:node:fetch-weather","type":"used_in"}
  ]
}

Минимальные поля: id, type, title; для FLOW_EDGE добавить from_node, to_node в data.

⸻

Генерация контента

Навигация (mkdocs.yml)
	•	Корневое меню:
	•	Overview
	•	PRD
	•	CJM
	•	User Flow
	•	User Stories
	•	HIG Patterns
	•	Global UX Principles
	•	Contextual UX
	•	По разделам — автогенерация nav: из сгенерированных файлов.

Страницы и шаблоны

1) Overview (docs/index.md)
	•	Сводка статусов: кол-во секций, стадий, узлов, историй, локальных принципов.
	•	Блок «Покрытие»: краткие числа из валидатора (если доступны).
	•	Диаграмма «Ландшафт» (сгенерированный SVG санкей/кластер из graph.json).
	•	Ссылки на ключевые отчёты.

2) PRD (docs/prd/*.md)
	•	Одна страница на секцию (ID и заголовок).
	•	Поля: цели, метрики, acceptance, refs.
	•	Секция «Связи»: ссылки на CJM стадии, сторис, узлы Flow, UX-принципы (по graph.json).

3) CJM (docs/cjm/*.md)
	•	Одна страница на стадию.
	•	Барьеры/возможности/метрики.
	•	«Отображение на Flow»: список узлов/рёбер + мини-диаграмма подграфа.

4) User Flow
	•	docs/flow/overview.md — общая диаграмма графа (DOT→SVG). Кластеры по CJM.
	•	docs/flow/nodes/*.md — страница на узел:
	•	ID, роль, inputs/outputs/guards, analytics, refs (PRD/CJM/Stories).
	•	Авто-ссылки на входящие/исходящие рёбра.
	•	docs/flow/edges/*.md (опционально) — если нужно.

5) User Stories (docs/stories/us-*.md)
	•	Одна страница на сторис:
	•	Role / Value / AC / Metrics.
	•	«Задействует»: PRD секции, Flow узлы/рёбра, HIG-кандидаты, CtxUX экраны.

6) HIG Patterns (docs/hig/*.md)
	•	По сторис: список кандидатов с pros/cons, SwiftUI примитивы, ссылки на принципы.

7) Global UX Principles (docs/ux/*.md)
	•	Принцип: описание, rationale, примеры.
	•	Связанные: Anti-patterns, какие Local Principles его используют.

8) Contextual UX (docs/ctxux/*.md)
	•	По экрану: список Local Principles (id, текст), telemetry (валидные event ids), ссылки на соответствующие Flow-узлы, глобальные принципы, QA заметки.
	•	Внизу — «Open in Figma» (если есть map _links.json).

⸻

Диаграммы

Обязательные
	1.	User Flow — docs/_media/userflow.svg
	•	DOT кластеры по CJM стадиям.
	•	Ноды — экраны/состояния, рёбра — события.
	•	Каждый элемент кликабелен и ведёт на страницу (href из slug).
	2.	Покрытие PRD→…→CtxUX — docs/_media/coverage.svg
	•	Санкей/сводная диаграмма (можно Graphviz cluster+edges).
	•	Переходы: PRD→CJM→Flow→Stories→HIG→CtxUX.
	•	Клики ведут на соответствующие страницы.

Опциональные (MVP+)
	•	Карта аналитики: event → узлы-эмиттеры.
	•	Тепловая карта «осиротевших» сущностей (если появятся).

⸻

Линки «Edit this page»
	•	Внизу каждой страницы: «✏️ Edit source».
	•	Ссылка не на _build, а на модульный источник:
	•	Узлы Flow → specs/02_userflow/nodes/<domain>.json (с якорем по id).
	•	Сторис → specs/04_userstories/us/<id>.json.
	•	Принципы → specs/03_ux_principles/principles/<id>.json.
	•	Экраны → specs/06_ctxux/screens/<screen-id>.json.
	•	Для якорей добавить генерацию #L<number> (не всегда стабильно) или «поисковую» ссылку с параметром ?plain=1#id:<...> если платформа поддерживает; в противном случае — просто на файл.

⸻

Генератор docs/generate_docs.py (ТЗ)

Функции:
	1.	load_build_artifacts() — читает все _build/*.json.
	2.	load_graph() — читает graph.json.
	3.	slugify(id) — общая функция для ссылок/имен файлов.
	4.	Рендер Markdown по Jinja-шаблонам:
	•	render_prd_sections(), render_cjm_stages(), render_flow(), render_stories(), render_hig(), render_ux(), render_ctxux().
	5.	render_graphs() — генерит DOT и вызывает Graphviz → SVG:
	•	userflow.dot → userflow.svg
	•	coverage.dot → coverage.svg
	6.	Проверки:
	•	warn, если узел/история/экран не имеет входящих связей (подсвечивать осиротевшие).
	7.	Итог: пишет MD в соответствующие папки, обновляет mkdocs.yml.nav (можно собрать список автоматически и записать YAML).

Зависимости:

pip install mkdocs mkdocs-material jinja2 pydot graphviz markdownify
brew/apt install graphviz


⸻

CI / GitHub Actions (.github/workflows/spechub.yml)
	•	Триггеры: push в main, PR.
	•	Шаги:
	1.	python3 specs/_build/build.py (сборка артефактов)
	2.	python3 trace_validator.py (гейт по fatal)
	3.	pip install зависимостей генератора
	4.	python3 docs/generate_docs.py
	5.	mkdocs build (на PR) и deploy на gh-pages (на main)
	•	Артефакты: загрузить /site и /docs/_media/*.svg в PR.

⸻

Правила кросс-ссылок
	•	Везде используем стабильные ID из IDs_LOCK.json.
	•	Генератор строит ссылку по типу сущности:
	•	PRD:4_2 → /prd/4_2/
	•	CJM:daily-logging → /cjm/daily-logging/
	•	FLOW:node:entry-editor → /flow/nodes/entry-editor/
	•	STORY:us-12 → /stories/us-12/
	•	HIG:us-12:candidate:sheet → /hig/us-12/#sheet
	•	UX:principle:one-screen-one-action → /ux/principles/one-screen-one-action/
	•	CTXUX:screen:documents-view → /ctxux/documents-view/

⸻

Безопасность и данные
	•	Не отображаем PII-поля (как project_name/project_location) в аналитике; только в разделе узла Outputs.
	•	В диаграммы не выводить значения, только ID/заголовки.
	•	Все данные — read-only из _build.

⸻

MVP → DoD (Definition of Done)

MVP (обязательно):
	•	Генератор MD + две диаграммы (userflow.svg, coverage.svg).
	•	Разделы: PRD, CJM, Flow (узлы), Stories, UX, HIG, CtxUX (по текущим 2 экранам).
	•	Все страницы содержат блок «Связи» с кликабельными ссылками.
	•	Кнопка «Edit source» ведёт к модульному файлу.
	•	CI собирает и публикует сайт на GitHub Pages.
	•	README с инструкцией локального запуска:
	•	python3 specs/_build/build.py
	•	python3 docs/generate_docs.py
	•	mkdocs serve

Nice-to-have (после MVP):
	•	Матрицы покрытия как таблицы (PRD↔Stories, Flow↔CtxUX).
	•	Фильтры по тегам/доменам (через JS-поиск темы).
	•	Отчёт «Orphans» — отдельная страница со списком несвязанных артефактов.

⸻

Приёмочные критерии
	•	Все артефакты текущего проекта отображаются и взаимно кликабельны.
	•	Диаграмма Flow открывается, элементы ведут на страницы узлов/рёбер.
	•	Нулевая деградация: при добавлении новой истории/экрана в модульных файлах сайт обновляется одной командой (build → generate → mkdocs).
	•	CI успешно публикует сайт; PR показывает артефакты (SVG) в комментарии.

⸻

План работ (итерации)
	1.	Экспорт graph.json в build.py.
	2.	Скелет docs/, mkdocs.yml, шаблоны Jinja.
	3.	Реализация docs/generate_docs.py (PRD/CJM/Flow/Stories).
	4.	Диаграммы (Flow, Coverage) + кликабельные href.
	5.	Разделы UX/HIG/CtxUX.
	6.	CI + Pages.
	7.	Полировка навигации, «Edit source», README.

⸻

Примечания по качеству
	•	В диаграммах избегать перегруза: группировать по стадиям, сворачивать редко используемые ветки.
	•	Для больших таблиц — пагинация/оглавление на странице.
	•	Консистентные слаги (нижний регистр, - вместо пробелов).

Если ок — можно сразу брать это ТЗ в работу.