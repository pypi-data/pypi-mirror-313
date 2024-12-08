.DEFAULT_GOAL := help

PYTHONPATH=
SHELL=bash
VENV=.venv


VENV_BIN=$(VENV)/bin


.venv:  ## Activate the virtual environment, creating it if it doesn't exist
	@if [ ! -d "$(VENV)" ]; then \
		uv venv $(VENV); \
		echo "Virtual environment created at $(VENV)"; \
	else \
		echo "Virtual environment already exists at $(VENV)"; \
	fi

	source $(VENV_BIN)/activate

.PHONY: sync
sync:  ## Sync the virtual environment
	$(MAKE) .venv

	uv sync --all-groups

	@echo "Virtual environment setup complete."

.PHONY: lint
lint:  ## Run linting checks
	uv run ruff check .
	uv run ruff format --check
	uv run pyright

.PHONY: format
format:  ## Run code formatting
	uv run ruff check . --fix
	uv run ruff format .

.PHONY: test
test:  ## Run tests
	uv run pytest

.PHONY: test-cov
test-cov:  ## Run tests and generate coverage report
	uv run pytest --cov --cov-report=html

.PHONY: open-cov
open-cov:  ## Open the coverage report in the browser
	uv run python -m webbrowser "file://$$(pwd)/htmlcov/index.html"

.PHONY: repl
repl:  ## Run a repl
	uv run ipython

.PHONY: help
help:  ## Display this help screen
	@echo -e "\033[1mAvailable commands:\033[0m"
	@grep -E '^[a-z.A-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2}' | sort