export PROJECT := tuxrun
export TUXPKG_MIN_COVERAGE := 96
export TUXPKG_FLAKE8_OPTIONS := --ignore=E203,E501,W503
check: typecheck test spellcheck stylecheck

include $(shell tuxpkg get-makefile)

.PHONY: htmlcov tags

htmlcov:
	python3 -m pytest --cov=tuxrun --cov-report=html

stylecheck: style flake8

spellcheck:
	codespell \
		-I codespell-ignore-list \
		--check-filenames \
		--skip '.git,public,dist,*.sw*,*.pyc,tags,*.json,.coverage,htmlcov,*.jinja2,*.yaml'

integration:
	python3 test/integration.py --devices "qemu-*" --tests ltp-smoke
	python3 test/integration.py --devices "fvp-aemva" --tests ltp-smoke

doc: docs/index.md
	mkdocs build

docs/index.md: README.md scripts/readme2index.sh
	scripts/readme2index.sh $@

doc-serve:
	mkdocs serve

flit = flit
publish-pypi:
	$(flit) publish

tags:
	ctags -R tuxrun/ test/

release: integration
