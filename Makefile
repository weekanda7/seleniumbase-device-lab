.PHONY: up down logs ps reset

# --wait blocks until every healthcheck is green (CI uses the same command).
up:
	docker compose up -d --build --wait

# -v drops the DB volume, so the next `up` starts from the 3 seed devices again.
down:
	docker compose down -v

logs:
	docker compose logs -f

ps:
	docker compose ps

reset: down up

# Lint both apps (each has its own `make lint`).
.PHONY: lint lint-check
lint:
	$(MAKE) -C backend lint
	$(MAKE) -C frontend lint
	$(MAKE) -C tests lint

lint-check:
	$(MAKE) -C backend lint-check
	$(MAKE) -C frontend lint-check
	$(MAKE) -C tests lint-check

# Tests are their own uv project in tests/ (black-box: they only talk to :8080 / :8000 / :5433).
# Needs `make up` first. Pass extra pytest args with ARGS, e.g. make test ARGS="-m ui -n auto"
.PHONY: test test-headed
test:
	cd tests && uv run pytest --headless $(ARGS)

test-headed:
	cd tests && uv run pytest --headed $(ARGS)
