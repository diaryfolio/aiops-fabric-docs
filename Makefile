.PHONY: docs-build docs-preview

docs-build:
	bash scripts/build-docs.sh

docs-preview: docs-build
	python3 -m http.server 8765 --bind 127.0.0.1 --directory site
