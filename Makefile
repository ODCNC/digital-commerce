VIRTUAL_ENV ?= .venv
ACTIVATE := . ${VIRTUAL_ENV}/*/activate

all:
	test -e .git/hooks/pre-commit || make pre-commit
	test -d ${VIRTUAL_ENV} || make venv
	make install-dev
venv:
	test -d ${VIRTUAL_ENV} || python -m venv ${VIRTUAL_ENV}
	${ACTIVATE} && pip install pip-tools pre-commit wheel
install-dev: install-r
	${ACTIVATE} && pip install -r requirements-dev.txt
install-r:
	test -e requirements.in || pip-compile
	${ACTIVATE} && pip install -r requirements.txt
pip-compile: ${VIRTUAL_ENV}
	pip install pip-tools
	pip-compile
pre-commit:
	pip install pre-commit
	pre-commit autoupdate
	pre-commit install
test: ${VIRTUAL_ENV} requirements.txt
	${ACTIVATE} && python -m pytest
