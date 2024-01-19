PROJECT_NAME="podium-api"

# keeps the shell context so virtualenv works properly
.ONESHELL:

# https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| sort | awk 'BEGIN {FS = ":.*?## "}; { printf "\033[36m%-15s\033[0m %s\n", $$1, $$2 }'

.PHONY: develop
develop: check-env ## Some helpful things to set up a dev environment
	. ${PYENV_VIRTUAL_ENV}/bin/activate
	pip install -r requirements.txt

check-env:
#	git config core.hooksPath .githooks
ifndef PYENV_VIRTUAL_ENV
		$(error pyenv virtual environment is not active)
endif

.PHONY: black
black: check-env ## Restyle with 'black'
	. ${PYENV_VIRTUAL_ENV}/bin/activate
	python -m black -l 120 . 

.PHONY: isort
isort: check-env ## Sort imports with isort
	. ${PYENV_VIRTUAL_ENV}/bin/activate
	python -m isort . --profile black --force-alphabetical-sort-within-sections

.PHONY: flake8
flake8: check-env ## lint check with flake8
	. ${PYENV_VIRTUAL_ENV}/bin/activate
	python -m flake8

.PHONY: mypy
mypy: check-env ## Static type checking with mypy
	. ${PYENV_VIRTUAL_ENV}/bin/activate
	python -m mypy . --disallow-untyped-defs --ignore-missing-imports

.PHONY: test
test: check-env ## Run fitness functions and automated tests
	. ${PYENV_VIRTUAL_ENV}/bin/activate
	python runtests.py

.PHONY: dist
dist: check-env test ## Deploy to pip repository via twine
	. ${PYENV_VIRTUAL_ENV}/bin/activate
	rm dist/*
	python setup.py sdist

.PHONY: tidy
tidy: black isort ## Tidy code
