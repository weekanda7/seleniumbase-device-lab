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

# ---- Images on GHCR (backend / web = the app, tests = the test runner) ----
# Version = git tag only (no VERSION file): v0.1.0 on a tagged commit, v0.1.0-3-gabc1234 after it.
# Multi-arch (amd64 + arm64) images are built by GitHub Actions on native runners (.github/workflows/images.yml),
# not on this laptop: emulating amd64 on Apple Silicon (QEMU) segfaults `uv sync`.
REGISTRY ?= ghcr.io/weekanda7
VERSION  ?= $(shell git describe --tags --always --dirty)
TAG      ?= latest
IMAGES   := backend web tests
CTX_backend := backend
CTX_web     := frontend
CTX_tests   := tests

.PHONY: version build release pull test-image

version:
	@echo $(VERSION)

# Local build for this machine's CPU only, loaded into local Docker (nothing is pushed).
build: $(addprefix build-,$(IMAGES))

build-%:
	docker build -t $(REGISTRY)/device-lab-$*:$(VERSION) $(CTX_$*)

# Release: tag the commit, then `make release` pushes the tag -> CI builds and pushes :<tag> and :latest.
release:
	@case "$(VERSION)" in *dirty*) echo "Uncommitted changes: commit first"; exit 1;; esac
	@git describe --tags --exact-match >/dev/null 2>&1 || { echo "HEAD has no tag: git tag vX.Y.Z first"; exit 1; }
	git push origin $(VERSION)

# make pull            -> :latest
# make pull TAG=v0.1.0 -> a fixed version
pull: $(addprefix pull-,$(IMAGES))

pull-%:
	docker pull $(REGISTRY)/device-lab-$*:$(TAG)

# Smoke-check the tests image: run API / DB tests inside it against the local stack (needs `make up`).
# Code is mounted, not baked in. UI tests come later with the Grid container.
# Local build: make test-image TAG=$$(make -s version)
test-image:
	docker run --rm -v $(CURDIR)/tests:/tests \
		--add-host=host.docker.internal:host-gateway \
		-e API_URL=http://host.docker.internal:8000/api \
		-e DB_DSN=postgresql://devicelab:devicelab@host.docker.internal:5433/devicelab \
		$(REGISTRY)/device-lab-tests:$(TAG) \
		pytest -m "api or db" -p no:cacheprovider
