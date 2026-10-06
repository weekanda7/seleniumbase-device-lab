FROM python:3.12-slim

WORKDIR /app
RUN pip install --no-cache-dir uv

# Dependencies first so this layer is cached when only app code changes.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

# Version from git (passed by Makefile / compose / CI). After the deps layer so it doesn't bust that cache.
ARG APP_VERSION=dev
ARG GIT_SHA=unknown
ENV APP_VERSION=$APP_VERSION GIT_SHA=$GIT_SHA

COPY app ./app

EXPOSE 8000
CMD ["uv", "run", "--no-sync", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
