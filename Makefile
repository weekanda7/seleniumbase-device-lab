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

lint-check:
	$(MAKE) -C backend lint-check
	$(MAKE) -C frontend lint-check
