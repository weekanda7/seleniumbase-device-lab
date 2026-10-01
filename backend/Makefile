.PHONY: install lint lint-check run

install:
	uv sync

# Local: fix what can be fixed, then format.
lint:
	uv run ruff check --fix .
	uv run ruff format .

# CI: report only, fail on any issue.
lint-check:
	uv run ruff check .
	uv run ruff format --check .

# Run against the compose DB (make up at repo root first, or at least the db service).
run:
	uv run uvicorn app.main:app --reload
