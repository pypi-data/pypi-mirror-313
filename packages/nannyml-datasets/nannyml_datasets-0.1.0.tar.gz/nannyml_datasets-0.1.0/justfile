alias b := build

app_version := `awk -F' = ' '/^version/ { gsub(/"/, "", $2); print $2 }' pyproject.toml`

install:
    uv sync --all-extras --dev

bump version="patch":
    uv run bump2version {{version}}

run:
    uv run python -m there_yet

debug:
    DEBUG=True uv run python -m there_yet

test:
    uv run pytest tests

build:
    uv run ruff check 
    uv build
