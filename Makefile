.PHONY: all help install dev run test fmt lint build clean run-autopilot

VENV_DIR    := .venv
PYTHON      := $(VENV_DIR)/bin/python
PIP         := $(VENV_DIR)/bin/pip
INSTALL_STAMP := $(VENV_DIR)/.installed.stamp
DEV_STAMP   := $(VENV_DIR)/.dev-deps.stamp

# Default target
all: dev ## Run the dev target by default

help: ## ✨ Display this help screen
	@echo "Available commands:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# --- Core Dependencies ---
# Creates venv if missing
$(PYTHON):
	@echo "Creating virtual environment in $(VENV_DIR)..."
	python3 -m venv $(VENV_DIR)
	@echo "Bootstrapping pip & wheel..."
	$(PIP) install -U pip wheel

# Installs project dependencies if pyproject.toml has changed
$(INSTALL_STAMP): pyproject.toml | $(PYTHON)
	@echo "Installing project dependencies..."
	$(PIP) install -e .
	@touch $(INSTALL_STAMP)

# Installs dev dependencies if requirements-dev.txt has changed
$(DEV_STAMP): requirements-dev.txt | $(PYTHON)
	@echo "Installing/updating dev dependencies..."
	$(PIP) install -r requirements-dev.txt
	@touch $(DEV_STAMP)

install: $(INSTALL_STAMP) ## 📦 Install project dependencies

dev: install $(DEV_STAMP) ## 🛠️  Create venv and install all project & dev dependencies

# --- Development Tasks ---
run: dev ## 🚀 Start the Matrix Guardian server
	@echo "Starting Matrix Guardian server..."
	UVICORN_WORKERS=$${UVICORN_WORKERS:-2} $(PYTHON) -m uvicorn guardian.main:app --host 0.0.0.0 --port 8000 --proxy-headers

test: dev ## 🧪 Run tests
	@echo "Running tests..."
	$(PYTHON) -m pytest

fmt: ## 💅 Format code with Ruff
	@echo "Formatting code with Ruff..."
	ruff format .
	ruff check --fix .

lint: ## 🔬 Lint code with Ruff
	@echo "Linting code with Ruff..."
	ruff check .

build: ## 🐳 Build the Docker image
	@echo "Building Docker image..."
	docker build -f infra/docker/Dockerfile -t matrix-guardian:latest .

clean: ## 🧹 Clean up generated files and directories
	@echo "Cleaning up..."
	rm -rf .venv __pycache__ .pytest_cache .mypy_cache dist build *.egg-info
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	@echo "Done."

# >>> AUTOPILOT: run target
run-autopilot: dev ## 🤖 Run the Autopilot worker
	@echo "Starting Autopilot worker..."
	$(PYTHON) -m guardian.runner.autopilot_worker
# <<< AUTOPILOT: run target