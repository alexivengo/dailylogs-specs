# SpecHub convenience targets

.PHONY: build validate docs serve all

build:
	python3 specs/_build/build.py

validate:
	python3 trace_validator.py

docs:
	python3 docs/generate_docs.py

serve:
	mkdocs serve

all: build validate docs
