.PHONY: setup run lint test clean format

setup:
	uv sync

run:
	uv run uvicorn nbry_lifting_website.app:app --reload

lint:
	uv run ruff check .

test:
	uv run pytest

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

format:
	uv run ruff check --fix .
	uv run ruff format .
	npx prettier@latest --plugin=prettier-plugin-jinja-template --parser=jinja-template --write "src/**/*.html"
