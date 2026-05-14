# Python Project Template

Modern Python setup using `uv`, `ruff`, `pytest`, and optional `direnv` + `Makefile`.

This project is designed to feel like modern tooling (Node/Rust style):

* reproducible environments
* fast dependency management
* minimal activation friction
* consistent linting + formatting

## Requirements

* Python 3.12+ (managed via `uv`)
* `uv`
* (optional) `direnv`
* (optional) `make`

## Setup

### Install dependencies

```bash
uv sync
```

This will:

* create/update the virtual environment
* install dependencies
* generate `uv.lock`

### Optional: auto environment activation

If using `direnv`, create `.envrc`:

```bash
source .venv/bin/activate
```

Then:

```bash
direnv allow
```

## Running

### Run application

```bash
uv pip install -e .
uv run python -m my_project.main
```

### Run tests

```bash
uv run pytest
```

## Code quality

### Lint

```bash
uv run ruff check .
```

### Format

```bash
uv run ruff format .
```

## Development workflow

```bash
uv sync
uv run pytest
uv run ruff check .
uv run ruff format .
```

Or (if Makefile is used):

```bash
make test
make lint
make format
```

## Project structure

```txt
.
├── app/
├── tests/
├── pyproject.toml
├── uv.lock
├── .python-version
├── .envrc
└── README.md
```

# Links

Quick reference for tools used in this project.

## Core tools

* uv (Python package + environment manager)
  [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)

* direnv (automatic environment loading per directory)
  [https://direnv.net/](https://direnv.net/)

* ruff (linting + formatting)
  [https://docs.astral.sh/ruff/](https://docs.astral.sh/ruff/)

* pytest (testing framework)
  [https://docs.pytest.org/](https://docs.pytest.org/)

## Optional tools

* make (task runner / scripting standard in many backend teams)
  [https://www.gnu.org/software/make/](https://www.gnu.org/software/make/)

## Useful commands (cheat sheet)

```bash
uv sync              # install dependencies
uv add <pkg>         # add dependency
uv add --dev <pkg>   # add dev dependency
uv run <command>     # run inside environment

direnv allow         # enable directory auto-env
```

## Notes

* `uv.lock` should be committed
* `.venv/` should NOT be committed
* `ruff` replaces black + flake8 in most modern setups
* `direnv` is optional but recommended for smoother DX
