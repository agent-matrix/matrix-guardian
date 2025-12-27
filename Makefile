# ═══════════════════════════════════════════════════════════════════════════════
# Matrix Guardian - Production-Ready Makefile
# Author: Ruslan Magana (ruslanmv.com)
# License: Apache 2.0
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: help install dev test lint fmt clean run run-autopilot \
        build docker-up docker-down pre-commit typecheck coverage \
        docs security audit upgrade release

# ═══════════════════════════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════════════════════════

# Colors for terminal output
BLUE := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
RESET := \033[0m

# Project configuration
PROJECT_NAME := matrix-guardian
PYTHON_VERSION := 3.11
UVICORN_WORKERS := 2
UVICORN_HOST := 0.0.0.0
UVICORN_PORT := 8000

# Paths
SRC_DIR := src
TEST_DIR := tests
DOCS_DIR := docs
DOCKER_DIR := infra/docker

# UV will manage virtual environments automatically
# If UV is not available, fallback to pip
UV := $(shell command -v uv 2> /dev/null)

# ═══════════════════════════════════════════════════════════════════════════════
# Help Target (Default)
# ═══════════════════════════════════════════════════════════════════════════════

help: ## 📚 Display this comprehensive help message
	@echo ""
	@echo "$(BLUE)════════════════════════════════════════════════════════════════$(RESET)"
	@echo "$(GREEN)  $(PROJECT_NAME) - Production-Ready Makefile$(RESET)"
	@echo "$(BLUE)════════════════════════════════════════════════════════════════$(RESET)"
	@echo ""
	@echo "$(YELLOW)Available Commands:$(RESET)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(BLUE)%-20s$(RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(BLUE)════════════════════════════════════════════════════════════════$(RESET)"
	@echo "$(YELLOW)Quick Start:$(RESET)"
	@echo "  1. $(GREEN)make install$(RESET)        - Install production dependencies"
	@echo "  2. $(GREEN)make dev$(RESET)            - Install all dependencies (prod + dev)"
	@echo "  3. $(GREEN)make test$(RESET)           - Run test suite"
	@echo "  4. $(GREEN)make run$(RESET)            - Start the API server"
	@echo ""
	@echo "$(YELLOW)Author:$(RESET)  Ruslan Magana (ruslanmv.com)"
	@echo "$(YELLOW)License:$(RESET) Apache 2.0"
	@echo "$(BLUE)════════════════════════════════════════════════════════════════$(RESET)"
	@echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# Installation Targets
# ═══════════════════════════════════════════════════════════════════════════════

install: ## 📦 Install production dependencies using UV
	@echo "$(GREEN)Installing production dependencies...$(RESET)"
ifdef UV
	@echo "$(BLUE)Using UV for fast package installation$(RESET)"
	uv pip install -e .
else
	@echo "$(YELLOW)UV not found, using pip (install UV for faster builds: pip install uv)$(RESET)"
	pip install -e .
endif
	@echo "$(GREEN)✓ Production dependencies installed$(RESET)"

dev: ## 🛠️  Install all dependencies (production + development) using UV
	@echo "$(GREEN)Installing all dependencies (production + development)...$(RESET)"
ifdef UV
	@echo "$(BLUE)Using UV for fast package installation$(RESET)"
	uv pip install -e ".[dev,types]"
else
	@echo "$(YELLOW)UV not found, using pip (install UV for faster builds: pip install uv)$(RESET)"
	pip install -e ".[dev,types]"
endif
	@echo "$(GREEN)✓ All dependencies installed$(RESET)"

upgrade: ## ⬆️  Upgrade all dependencies to latest compatible versions
	@echo "$(GREEN)Upgrading dependencies...$(RESET)"
ifdef UV
	uv pip install --upgrade -e ".[dev,types]"
else
	pip install --upgrade -e ".[dev,types]"
endif
	@echo "$(GREEN)✓ Dependencies upgraded$(RESET)"

# ═══════════════════════════════════════════════════════════════════════════════
# Development & Runtime Targets
# ═══════════════════════════════════════════════════════════════════════════════

run: ## 🚀 Start the Matrix Guardian API server (FastAPI + Uvicorn)
	@echo "$(GREEN)Starting Matrix Guardian server...$(RESET)"
	@echo "$(BLUE)Server will be available at: http://$(UVICORN_HOST):$(UVICORN_PORT)$(RESET)"
	@echo "$(BLUE)Workers: $(UVICORN_WORKERS)$(RESET)"
	python -m uvicorn guardian.main:app \
		--host $(UVICORN_HOST) \
		--port $(UVICORN_PORT) \
		--workers $(UVICORN_WORKERS) \
		--proxy-headers \
		--log-level info

run-dev: ## 🔧 Start the server in development mode (auto-reload enabled)
	@echo "$(GREEN)Starting Matrix Guardian in development mode...$(RESET)"
	@echo "$(YELLOW)Auto-reload enabled - code changes will restart the server$(RESET)"
	python -m uvicorn guardian.main:app \
		--host 127.0.0.1 \
		--port $(UVICORN_PORT) \
		--reload \
		--log-level debug

run-autopilot: ## 🤖 Run the Autopilot worker (headless mode)
	@echo "$(GREEN)Starting Autopilot worker...$(RESET)"
	@echo "$(BLUE)Running in headless mode with policy enforcement$(RESET)"
	python -m guardian.runner.autopilot_worker

# ═══════════════════════════════════════════════════════════════════════════════
# Code Quality & Testing Targets
# ═══════════════════════════════════════════════════════════════════════════════

test: ## 🧪 Run the complete test suite with coverage
	@echo "$(GREEN)Running test suite...$(RESET)"
	pytest -v --cov=src/guardian --cov-report=term-missing --cov-report=html
	@echo "$(GREEN)✓ Tests complete. Coverage report: htmlcov/index.html$(RESET)"

test-quick: ## ⚡ Run tests without coverage (faster)
	@echo "$(GREEN)Running quick tests...$(RESET)"
	pytest -v -x
	@echo "$(GREEN)✓ Quick tests complete$(RESET)"

test-unit: ## 🎯 Run unit tests only
	@echo "$(GREEN)Running unit tests...$(RESET)"
	pytest -v -m unit
	@echo "$(GREEN)✓ Unit tests complete$(RESET)"

test-integration: ## 🔗 Run integration tests only
	@echo "$(GREEN)Running integration tests...$(RESET)"
	pytest -v -m integration
	@echo "$(GREEN)✓ Integration tests complete$(RESET)"

coverage: ## 📊 Generate detailed coverage report
	@echo "$(GREEN)Generating coverage report...$(RESET)"
	pytest --cov=src/guardian \
		--cov-report=html \
		--cov-report=term \
		--cov-report=xml \
		--cov-fail-under=80
	@echo "$(GREEN)✓ Coverage report generated$(RESET)"
	@echo "$(BLUE)  - HTML: htmlcov/index.html$(RESET)"
	@echo "$(BLUE)  - XML:  coverage.xml$(RESET)"

lint: ## 🔬 Lint code with Ruff (check only, no fixes)
	@echo "$(GREEN)Linting code with Ruff...$(RESET)"
	ruff check $(SRC_DIR) $(TEST_DIR)
	@echo "$(GREEN)✓ Linting complete$(RESET)"

fmt: ## 💅 Format code with Ruff (auto-fix issues)
	@echo "$(GREEN)Formatting code with Ruff...$(RESET)"
	ruff format $(SRC_DIR) $(TEST_DIR)
	ruff check --fix $(SRC_DIR) $(TEST_DIR)
	@echo "$(GREEN)✓ Code formatted$(RESET)"

typecheck: ## 🔍 Run static type checking with MyPy
	@echo "$(GREEN)Running type checking with MyPy...$(RESET)"
	mypy $(SRC_DIR)
	@echo "$(GREEN)✓ Type checking complete$(RESET)"

security: ## 🔒 Run security audit on dependencies
	@echo "$(GREEN)Running security audit...$(RESET)"
ifdef UV
	uv pip list --format=freeze | python -m pip_audit
else
	pip-audit
endif
	@echo "$(GREEN)✓ Security audit complete$(RESET)"

audit: security ## 🛡️  Alias for security audit

pre-commit: ## ✨ Run pre-commit hooks on all files
	@echo "$(GREEN)Running pre-commit hooks...$(RESET)"
	pre-commit run --all-files
	@echo "$(GREEN)✓ Pre-commit hooks complete$(RESET)"

pre-commit-install: ## 🔧 Install pre-commit Git hooks
	@echo "$(GREEN)Installing pre-commit hooks...$(RESET)"
	pre-commit install
	@echo "$(GREEN)✓ Pre-commit hooks installed$(RESET)"

# ═══════════════════════════════════════════════════════════════════════════════
# Docker Targets
# ═══════════════════════════════════════════════════════════════════════════════

build: ## 🐳 Build Docker image
	@echo "$(GREEN)Building Docker image...$(RESET)"
	docker build -f $(DOCKER_DIR)/Dockerfile -t $(PROJECT_NAME):latest .
	@echo "$(GREEN)✓ Docker image built: $(PROJECT_NAME):latest$(RESET)"

docker-up: ## 🚢 Start all services with Docker Compose
	@echo "$(GREEN)Starting Docker Compose services...$(RESET)"
	docker compose -f $(DOCKER_DIR)/compose.yaml up --build -d
	@echo "$(GREEN)✓ Services started$(RESET)"
	@echo "$(BLUE)API available at: http://localhost:8000$(RESET)"

docker-down: ## 🛑 Stop all Docker Compose services
	@echo "$(GREEN)Stopping Docker Compose services...$(RESET)"
	docker compose -f $(DOCKER_DIR)/compose.yaml down
	@echo "$(GREEN)✓ Services stopped$(RESET)"

docker-logs: ## 📋 Show Docker Compose logs
	@echo "$(GREEN)Showing Docker Compose logs...$(RESET)"
	docker compose -f $(DOCKER_DIR)/compose.yaml logs -f

docker-clean: ## 🧹 Remove Docker containers, volumes, and images
	@echo "$(RED)Removing Docker containers, volumes, and images...$(RESET)"
	docker compose -f $(DOCKER_DIR)/compose.yaml down -v --rmi all
	@echo "$(GREEN)✓ Docker cleanup complete$(RESET)"

# ═══════════════════════════════════════════════════════════════════════════════
# Cleanup Targets
# ═══════════════════════════════════════════════════════════════════════════════

clean: ## 🧹 Remove build artifacts, cache files, and temporary files
	@echo "$(GREEN)Cleaning up...$(RESET)"
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf coverage.xml
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.orig" -delete
	@echo "$(GREEN)✓ Cleanup complete$(RESET)"

clean-all: clean docker-clean ## 🗑️  Remove all artifacts including Docker resources
	@echo "$(GREEN)✓ Complete cleanup finished$(RESET)"

# ═══════════════════════════════════════════════════════════════════════════════
# Release & Deployment Targets
# ═══════════════════════════════════════════════════════════════════════════════

release: ## 🎉 Create a new release (build + tag)
	@echo "$(GREEN)Creating release...$(RESET)"
	@echo "$(YELLOW)Ensure version is updated in pyproject.toml$(RESET)"
	python -m build
	@echo "$(GREEN)✓ Release artifacts created in dist/$(RESET)"
	@echo "$(BLUE)Next steps:$(RESET)"
	@echo "  1. Review artifacts in dist/"
	@echo "  2. git tag -a v<version> -m 'Release v<version>'"
	@echo "  3. git push origin v<version>"
	@echo "  4. python -m twine upload dist/*"

# ═══════════════════════════════════════════════════════════════════════════════
# CI/CD Targets
# ═══════════════════════════════════════════════════════════════════════════════

ci: ## 🔄 Run full CI pipeline (install, lint, typecheck, test)
	@echo "$(GREEN)Running CI pipeline...$(RESET)"
	$(MAKE) dev
	$(MAKE) fmt
	$(MAKE) lint
	$(MAKE) typecheck
	$(MAKE) test
	@echo "$(GREEN)✓ CI pipeline complete$(RESET)"

# ═══════════════════════════════════════════════════════════════════════════════
# Development Utilities
# ═══════════════════════════════════════════════════════════════════════════════

shell: ## 🐚 Open an interactive Python shell with project context
	@echo "$(GREEN)Opening Python shell...$(RESET)"
	python -c "import sys; sys.path.insert(0, 'src'); import IPython; IPython.embed()"

check: ## ✅ Run all checks (lint + typecheck + test)
	@echo "$(GREEN)Running all checks...$(RESET)"
	$(MAKE) lint
	$(MAKE) typecheck
	$(MAKE) test
	@echo "$(GREEN)✓ All checks passed$(RESET)"

info: ## ℹ️  Display project information
	@echo ""
	@echo "$(BLUE)════════════════════════════════════════════════════════════════$(RESET)"
	@echo "$(GREEN)  Project Information$(RESET)"
	@echo "$(BLUE)════════════════════════════════════════════════════════════════$(RESET)"
	@echo "$(YELLOW)Name:$(RESET)        $(PROJECT_NAME)"
	@echo "$(YELLOW)Python:$(RESET)      $(PYTHON_VERSION)"
	@echo "$(YELLOW)Author:$(RESET)      Ruslan Magana"
	@echo "$(YELLOW)Website:$(RESET)     ruslanmv.com"
	@echo "$(YELLOW)License:$(RESET)     Apache 2.0"
	@echo ""
	@echo "$(YELLOW)Paths:$(RESET)"
	@echo "  Source:     $(SRC_DIR)"
	@echo "  Tests:      $(TEST_DIR)"
	@echo "  Docker:     $(DOCKER_DIR)"
	@echo ""
	@echo "$(YELLOW)Package Manager:$(RESET)"
ifdef UV
	@echo "  Using UV: $(shell uv --version)"
else
	@echo "  Using pip: $(shell pip --version | cut -d' ' -f2)"
endif
	@echo "$(BLUE)════════════════════════════════════════════════════════════════$(RESET)"
	@echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# Default target
# ═══════════════════════════════════════════════════════════════════════════════

.DEFAULT_GOAL := help
