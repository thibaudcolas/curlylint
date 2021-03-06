.PHONY: clean-pyc init help test-ci
.DEFAULT_GOAL := help

help: ## See what commands are available.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36mmake %-15s\033[0m # %s\n", $$1, $$2}'

init: clean-pyc ## Install dependencies and initialise for development.
	pip install --upgrade pip setuptools twine wheel
	pip install -e '.[dev]'

lint: ## Lint the project.
	black --check **/*.py
	flake8 **/*.py
	mypy curlylint

format: ## Format project files.
	black **/*.py
	npm run format

test: ## Test the project.
	pytest --strict-config

test-watch: ## Restarts the tests whenever a file changes.
	nodemon -q -e py,json -w curlylint  -x "clear && pytest --strict-config --exitfirst --new-first -q || true"

test-coverage: ## Run the tests while generating test coverage data.
	coverage run -m pytest --strict-config && coverage report && coverage html

clean-pyc: ## Remove Python file artifacts.
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

sdist: ## Builds package version
	rm dist/* ; python setup.py sdist bdist_wheel

publish: sdist ## Publishes a new version to pypi.
	twine upload dist/*

publish-test: sdist ## Publishes a new version to test pypi.
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*
