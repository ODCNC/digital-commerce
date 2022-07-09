all:
	test -e .git/hooks/pre-commit || make pre-commit
	make install-dev
install-dev:
	pip install poetry
	poetry install
pre-commit:
	poetry install pre-commit
	pre-commit autoupdate
	pre-commit install
test:
	PYTHONPATH=. poetry run pytest --cov-report term-missing --cov=odcnc tests
