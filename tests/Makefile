case_path=cases/*
n=1

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

pytest:
	${test_env} \
	pytest -s -q -k ${k} ${case_path} \
	-m "not install_case and not future_case" \
	--html=./report/report.html --self-contained-html \
	--junit-xml=./report/report.xml \
	${headed_mode}
.PHONY: pytest

local-test:
	@make pytest test_env="uv run" headed_mode="--headed"
.PHONY: local-test

local-test-headless:
	@make pytest test_env="uv run" headed_mode="--headless"
.PHONY: local-test-headless
