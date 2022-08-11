help: ## Display callable targets.
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

test: ## Run all tests.
	pytest

coverage: ## Run all tests and generate coverage report.
	coverage run --source=flask_sustainable -m pytest tests
	coverage html
	coverage report -m

requirements: ## Install requirements.
	pip install .

install: ## Install package.
	pip install -e .

run: ## Run a example script.
	export FLASK_APP=example.py FLASK_DEBUG=1 FLASK_ENV=development && flask run

format: ## Format code.
	docformatter --in-place -r **/*.py
	isort .
	black .

publish: ## Publish package to PyPI.
	# Need to setup env variables...
	# https://flit.pypa.io/en/latest/cmdline.html?highlight=publish#envvar-FLIT_USERNAME
	flit publish --setup-py