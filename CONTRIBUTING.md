# Contributing to DailyLogs Specs / SpecHub

## How to edit specs
- Edit modular JSON files under `specs/**` (PRD, CJM, User Flow, UX, User Stories, HIG, CtxUX).
- Keep IDs stable; cross-references use canonical forms like `PRD:#id`, `CJM:#id`, `FLOW:#node`, `us-*`.
- Validate locally before submitting a PR.

## Local run
```bash
python3 -m venv .venv
. .venv/bin/activate
pip install mkdocs mkdocs-material jinja2 pydot graphviz markdownify
python3 specs/_build/build.py
python3 trace_validator.py
python3 docs/generate_docs.py
mkdocs serve
```

## CI pipeline
- Build monoliths → Validate traces → Generate docs → MkDocs build (strict) → Link check → Deploy to GitHub Pages
- Schema badge is propagated to pages from validator result.

## Submitting changes
- Create a feature branch and open a PR.
- Ensure `mkdocs build --strict` passes locally.
- Include screenshots of the Overview and a short summary of changes.

## Structure reference
- Sources: `specs/**`
- Artifacts: `specs/_build/*.json`
- Docs output: `docs/**` (diagrams in `docs/_media/*.svg`)

## Contact
- Repository: https://github.com/alexivengo/dailylogs-specs
