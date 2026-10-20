---
name: index
description: Where things are defined in seleniumbase-device-lab — maps each kind of question (acceptance criteria, API, testids, page objects, test layout, CI / reports, MCP, environment, frontend, version) to its source-of-truth file. Read before answering any "where is X / what is Y called / how does Z work" question about this repo, and before grepping the tree.
---

# index — where is the spec?

One table. Find the row that matches your question and open that file **first**; it is the source of truth for that topic. If two files disagree, the entry file wins.

## Entry table

| Question | Open first (source of truth) | Path | Note |
|---|---|---|---|
| How should a feature behave? (acceptance criteria) | `features.md` — Gherkin F1–F7 + Device detail | `.claude/skills/device-lab-dev/references/features.md` | **Product spec = the judge**; triage decisions also follow it |
| Which APIs exist, fields, status codes | FastAPI OpenAPI | running app: `http://127.0.0.1:8000/docs`, `/openapi.json`; code in `backend/app/api/` | Black-box tests only talk to 8080 / 8000 / 5433 |
| How to locate an element, what a testid is called | `testid-spec` skill + mapping table | `.claude/skills/testid-spec/SKILL.md` (short version + this repo's table), `references/testid-spec.md` (full spec) | Name new UI elements by this before writing locators |
| How page actions are written (Page Objects) | `tests/pages/` | `login/login_page.py`, `device/device_list_page.py`, `device/device_form_page.py`, `device/device_detail_page.py`; shared in `pages/common/` | Static methods take `sb` |
| Test layering and how to run | README "Test design" / "Run it" + `tests/Makefile` | `README.md`, `tests/cases/{ui,api,db}/`, `tests/cases/conftest.py` (`api` fixture), `tests/base/` (NoAuthCase / AuthCase) | pytest marks + xdist |
| Clients used by API / DB tests | `tests/api_apiserver/`, `tests/db_client/` | `auth.py`, `devices.py`, `device_db.py` | DB access is read-only |
| AI runs a GWT; how to classify a fail | `gwt-run` skill + triage | `.claude/skills/gwt-run/SKILL.md`, `references/triage.md` (env → testid → test bug → product bug → unknown) | Logs in `tests/report/gwt/` |
| Rules for changing the app (layers, contract-first, DoD) | `device-lab-dev` skill | `.claude/skills/device-lab-dev/SKILL.md` | Layers: api / application / domain / infrastructure |
| Environment, ports, how to start | docker-compose + Makefile | `docker-compose.yml` (8080 web / 8000 backend / 5433 db, bound to 127.0.0.1), `Makefile` (up / down / test / release) | |
| What CI does, where reports are | workflows + gh-pages | `.github/workflows/ci.yml` (lint → images → tests → pages), `.github/workflows/images.yml` (tag → GHCR), reports: https://weekanda7.github.io/seleniumbase-device-lab/ | |
| How MCP is wired | `.mcp.json` + README "AI-driven runs" | `.mcp.json`, `tests` `mcp` dependency group | Pure CDP, no chromedriver |
| Frontend pages / i18n | `frontend/src/` | `pages/`, `components/`, `api.ts`, `i18n.ts` | F6 language switch |
| Version | `/api/version` + login page footer | README "Run it" (`make version`); F7 | UI asserts Web == API |

## Keep it in sync

- Adding a new source-of-truth file (a skill, a spec, a new test layer) → add a row here in the same commit.
- Each entry file should start with a one-line pointer back here (`> Entry index: .claude/skills/index/SKILL.md`) so the two cannot drift silently.
- This table only says *where*; it never duplicates the content. If a row needs more than one line of note, the note belongs in the entry file.
