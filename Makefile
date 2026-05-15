run:
	uvicorn nbry_lifting_website.app:app --reload

lint:
	uv run ruff check .

test:
	uv run pytest

format:
	uv run ruff check --fix .
	uv run ruff format .
	npx prettier@latest --plugin=prettier-plugin-jinja-template --parser=jinja-template --write "src/**/*.html"
