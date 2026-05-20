.PHONY: help setup install run run-master run-landing run-lifting run-mycareer run-dev lint test test-cov type-check format clean clean-cache db-up db-down db-logs docker-up docker-down docker-logs

# Default target
help:
	@echo "NBRY Multi-Site Platform - Available Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make setup          - Install dependencies with uv sync"
	@echo "  make install        - Alias for setup"
	@echo ""
	@echo "Run Applications:"
	@echo "  make run            - Run master app with subdomain routing (port 8000)"
	@echo "  make run-master     - Alias for run"
	@echo "  make run-landing    - Run landing site only (port 8000)"
	@echo "  make run-lifting    - Run lifting site only (port 8001)"
	@echo "  make run-mycareer   - Run career site only (port 8003)"
	@echo "  make run-dev        - Run landing (8000) and lifting (8001) in parallel"
	@echo ""
	@echo "Development:"
	@echo "  make lint           - Run ruff linter"
	@echo "  make test           - Run pytest"
	@echo "  make test-cov       - Run pytest with coverage report"
	@echo "  make type-check     - Run pyright type checker"
	@echo "  make format         - Auto-format code (ruff + prettier)"
	@echo "  make clean          - Remove Python cache files"
	@echo "  make clean-cache    - Remove all cache and build files"

# Setup
setup:
	uv sync

install: setup

# Run commands
run:
	uv run uvicorn nbry_website.main:app --reload --host 0.0.0.0 --port 8000

run-master: run

run-landing:
	uv run uvicorn nbry_website.sites.landing.app:app --reload --port 8000

run-lifting:
	uv run uvicorn nbry_website.sites.lifting.app:app --reload --port 8001

run-mycareer:
	uv run uvicorn nbry_website.sites.mycareer.app:app --reload --port 8003

run-dev:
	@echo "Starting landing (8000) and lifting (8001) sites..."
	@echo "Press Ctrl+C to stop both"
	@trap 'kill 0' INT; \
	uv run uvicorn nbry_website.sites.landing.app:app --reload --port 8000 & \
	uv run uvicorn nbry_website.sites.lifting.app:app --reload --port 8001 & \
	uv run uvicorn nbry_website.sites.mycareer.app:app --reload --port 8003 & \
	wait

# Development tools
lint:
	uv run ruff check .

test:
	uv run pytest

test-cov:
	uv run pytest --cov=src --cov-report=html --cov-report=term

type-check:
	uv run pyright src/

format:
	uv run ruff check --fix .
	uv run ruff format .
	npx prettier@latest --plugin=prettier-plugin-jinja-template --parser=jinja-template --write "src/**/*.html"

# Clean
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

clean-cache: clean
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf *.egg-info
	rm -rf dist
	rm -rf build
