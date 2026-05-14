# Project Summary

This setup gives you:

* fnm-like Python version switching
* automatic virtualenv activation (no `source activate`)
* modern dependency management (like npm / cargo)
* modern linting + formatting
* reproducible environments

---

# 1. Install core tools

## Install uv

[uv documentation](https://docs.astral.sh/uv/?utm_source=chatgpt.com)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## Install direnv

[direnv documentation](https://direnv.net/?utm_source=chatgpt.com)

### Fedora:

```bash
sudo dnf install direnv
```

---

## Enable direnv in your shell

### zsh:

```bash
echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc
source ~/.zshrc
```

---

# 2. Create a new Python project

```bash
mkdir my-project
cd my-project

uv init
```

This creates:

* `pyproject.toml`
* starter project files

---

# 3. Pin Python version (fnm-like behavior)

```bash
uv python pin 3.12
```

This creates:

```txt
.python-version
```

---

# 4. Create virtual environment

```bash
uv venv
```

This creates:

```txt
.venv/
```

---

# 5. Setup automatic environment activation

Create a `.envrc` file:

```bash
source .venv/bin/activate
```

Then allow direnv:

```bash
direnv allow
```

---

## Result

Now when you:

```bash
cd my-project
```

You automatically get:

* correct Python version
* virtualenv activated
* PATH configured

Leaving the directory cleans it up automatically.

---

# 6. Dependency management (npm-like)

## Add a dependency

```bash
uv add fastapi
```

## Add dev dependencies

```bash
uv add --dev ruff pyright pytest
```

---

## Install everything (if needed)

```bash
uv sync
```

---

# 7. Lock file (important)

uv automatically generates:

```txt
uv.lock
```

This is equivalent to:

* package-lock.json (npm)
* Cargo.lock (Rust)

---

# 8. Run commands (no activation needed)

Instead of activating venv manually:

```bash
uv run python main.py
uv run pytest
uv run ruff check .
```

---

# 9. Linting + formatting (modern standard)

## Ruff (recommended)

[Ruff documentation](https://docs.astral.sh/ruff/?utm_source=chatgpt.com)

Install:

```bash
uv add --dev ruff
```

### Format code

```bash
uv run ruff format .
```

### Lint code

```bash
uv run ruff check .
```

### Auto-fix issues

```bash
uv run ruff check . --fix
```

---

# 10. Type checking (recommended)

```bash
uv add --dev pyright
```

Run:

```bash
uv run pyright
```

---

# 11. Example project structure

```txt
my-project/
├── .python-version
├── .envrc
├── .venv/
├── pyproject.toml
├── uv.lock
├── src/
│   └── my_project/
├── tests/
└── README.md
```

---

# 12. Mental model (important)

| Node ecosystem    | Python ecosystem |
| ----------------- | ---------------- |
| fnm               | uv python pin    |
| npm install       | uv add           |
| package.json      | pyproject.toml   |
| package-lock.json | uv.lock          |
| node_modules      | .venv            |
| npm run           | uv run           |
| prettier/eslint   | ruff             |
| tsc               | pyright          |
| nvm use auto      | direnv           |

---

# Summary

This setup removes:

* manual `source venv/bin/activate`
* requirements.txt workflows
* inconsistent Python versions
* slow pip workflows

And replaces it with:

* reproducible environments
* automatic activation
* modern dependency graph + lockfile
* fast tooling (Rust-based where possible)

---

If you want next step, I can turn this into a **ready-to-clone project template repo** with:

* Makefile or justfile
* pre-commit hooks
* GitHub Actions CI
* pytest + coverage
* FastAPI or CLI scaffold

Basically: “cargo new” but for Python.

