.PHONY: all dev run test fmt lint build clean

VENV_DIR=.venv
PYTHON=$(VENV_DIR)/bin/python
PIP=$(VENV_DIR)/bin/pip

# Default target
all: dev

dev: $(VENV_DIR)/touchfile

$(VENV_DIR)/touchfile: pyproject.toml requirements-dev.txt
	@echo "Creating/updating virtual environment in $(VENV_DIR)..."
	python3 -m venv $(VENV_DIR)
	$(PIP) install -U pip wheel
	$(PIP) install -e .
	$(PIP) install -r requirements-dev.txt
	@touch $(VENV_DIR)/touchfile

run: dev
	@echo "Starting Matrix Guardian server..."
	UVICORN_WORKERS=$${UVICORN_WORKERS:-2} $(PYTHON) -m uvicorn guardian.main:app --host 0.0.0.0 --port 8000 --proxy-headers

test: dev
	@echo "Running tests..."
	$(PYTHON) -m pytest

fmt:
	@echo "Formatting code with Ruff..."
	ruff format .
	ruff check --fix .

lint:
	@echo "Linting code with Ruff..."
	ruff check .

build:
	@echo "Building Docker image..."
	docker build -f infra/docker/Dockerfile -t matrix-guardian:latest .

clean:
	@echo "Cleaning up..."
	rm -rf .venv __pycache__ .pytest_cache .mypy_cache dist build *.egg-info
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

# >>> AUTOPILOT: run target
run-autopilot: dev
	@echo "Starting Autopilot worker..."
	$(PYTHON) -m guardian.runner.autopilot_worker
# <<< AUTOPILOT: run target
