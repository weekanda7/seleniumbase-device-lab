.PHONY: install lint lint-check dev build

install:
	npm ci

# Local: auto-fix ESLint issues, then format with Prettier.
lint:
	npm run lint -- --fix
	npm run format

# CI: report only, fail on any warning or unformatted file.
lint-check:
	npm run lint
	npm run format:check

# Vite dev server on :5173, proxies /api to the backend on :8000.
dev:
	npm run dev

build:
	npm run build
