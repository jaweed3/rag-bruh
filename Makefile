SHELL := /bin/bash
UV := $(shell command -v uv 2> /dev/null)

.PHONY: help install-dev install run build up down logs smoke test quality clean seed

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install-dev:
	@if [ -z "$(UV)" ]; then echo "uv not found. Install uv firstly."; exit 1; fi
	uv sync --only-group dev

install:
	uv sync

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload

build:
	docker build -t library-rag .

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

seed:
	uv run python scripts/seed_data.py

smoke:
	bash scripts/smoke_test.sh

test:
	uv run pytest tests/ -v --cov=app --cov=core --cov-report=term-missing

quality:
	uv run ruff check .
	uv run ruff format --check .
	uv run mypy app/ core/ --ignore-missing-imports

clean:
	rm -rf artifacts/ runs/ __pycache__
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
