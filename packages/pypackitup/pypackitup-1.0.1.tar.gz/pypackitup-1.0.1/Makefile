# You can set these variables from the command line and also from the environment.
DOCS_OPTS    ?=
DOCS_BUILD   ?= mkdocs

# Determine this makefile's path. Be sure to place this BEFORE `include` directives, if any.
THIS_FILE := $(lastword $(MAKEFILE_LIST))

# Put it first so that "make" without argument is like "make help".
help:
	@$(DOCS_BUILD) -h $(DOCS_OPTS) $(O)

.PHONY: update lint secure test_code test_actions test_actions_amd build verify_build get_version set_version test_docs docs test_deploy deploy help Makefile

update: ## Update all package dependencies.
	uv sync --all-extras --dev

lint: ## Lint the package code with ruff.
	ruff check .

secure: ## Check package code security with bandit.
	bandit -c pyproject.toml -r .

test_code: ## Run code tests with Pytest.
	pytest tests

test_actions: ## Test package GitHub Actions using act.
	act -j build

test_actions_amd: ## Test package GitHub Actions on ARM architecture using act.
	act --container-architecture linux/amd64 -j build

build: update lint secure test_code ## Build PyPI packages for distribution.
	uv build

verify_build: ## Check PyPI packages for issues.
	twine check dist/*

get_version: ## Extract Python package version from VERSION.py
	echo $$(python -c "from VERSION import __version__; print(f'v{__version__}')")

set_version: ## Set Python package version in VERSION.py using latest git tag
	python scripts/update_docs_for_github_pages.py

test_docs: ## Extract Python package version and serve MkDocs documentation locally for testing.
	export PYTHON_PACKAGE_VERSION=$$(python -c "from VERSION import __version__; print(f'v{__version__}')") && mkdocs serve

docs: set_version build ## Extract Python package version and build MkDocs documentation for distribution.
	export PYTHON_PACKAGE_VERSION=$$(python -c "from VERSION import __version__; print(f'v{__version__}')") && mkdocs build

test_deploy: docs verify_build ## Deploy PyPI package to Test PyPI with Twine.
	twine upload -r testpypi dist/*

uv_test_deploy: docs verify_build ## Deploy PyPI package to Test PyPI with uv.
	export UV_PUBLISH_URL=https://test.pypi.org/legacy/ && export UV_PUBLISH_TOKEN=$$(python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.environ.get('TEST_UV_PUBLISH_TOKEN'))") && uv publish

deploy: docs verify_build ## Deploy PyPI package to PyPI with Twine.
	twine upload dist/*

uv_deploy: docs verify_build ## Deploy PyPI package to PyPI with uv.
	export UV_PUBLISH_URL=https://upload.pypi.org/legacy/ && export UV_PUBLISH_TOKEN=$$(python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.environ.get('UV_PUBLISH_TOKEN'))") && uv publish
