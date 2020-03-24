.PHONY: clean-pyc init help test-ci
.DEFAULT_GOAL := help

help: ## See what commands are available.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36mmake %-15s\033[0m # %s\n", $$1, $$2}'

init: clean-pyc ## Install dependencies and initialise for development.
	pip install --upgrade pip setuptools twine
	pip install pipenv pycodestyle
	pipenv install --dev

clean-pyc: ## Remove Python file artifacts.
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

sdist: ## Builds package version
	rm dist/* ; python setup.py sdist

publish: sdist ## Publishes a new version to pypi.
	twine upload dist/* && echo 'Success! Go to https://pypi.org/project/curlylint/ and check that all is well.'

publish-test: sdist ## Publishes a new version to test pypi.
	twine upload --repository-url https://test.pypi.org/legacy/ dist/* && echo 'Success! Go to https://test.pypi.org/project/curlylint/ and check that all is well.'
