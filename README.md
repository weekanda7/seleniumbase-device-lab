# seleniumbase-device-lab

[![CI](https://github.com/weekanda7/seleniumbase-device-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/weekanda7/seleniumbase-device-lab/actions/workflows/ci.yml)

A small device-management web app (FastAPI + PostgreSQL + React) used as the system under test
for a SeleniumBase / API / DB test suite.

> Work in progress — tests, CI and the full README come next.

## Run it

Requires Docker.

```bash
make up      # build + start db, backend, web; waits until all healthchecks pass
make down    # stop and wipe the DB (next `up` starts from the 3 seed devices)
```

| URL | What |
|---|---|
| http://localhost:8080 | Web UI (login: see `.env.example`) |
| http://localhost:8000/docs | API docs (Swagger) |
| `localhost:5433` | PostgreSQL (`devicelab` / `devicelab`) |

## Layout

```
backend/   FastAPI app — api / application / domain / infrastructure layers
frontend/  React + Vite SPA, served by nginx (proxies /api to the backend)
docker-compose.yml
```
