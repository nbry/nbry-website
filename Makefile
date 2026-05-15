run:
	uvicorn nbry_lifting_website.app:app --reload

lint:
	uv run ruff check .

format:
	uv run ruff check --fix .
	uv run ruff format .
	npx prettier --write "src/**/*.{html,css}"
