# Test runner image: Python + uv + the test dependencies only.
# - Test code is NOT copied in: it is mounted at run time (-v $(CURDIR)/tests:/tests),
#   so this image only needs a rebuild when pyproject.toml / uv.lock change.
# - No browser inside: UI tests will talk to a Selenium Grid container (--server / --port).
FROM python:3.12-slim

RUN pip install --no-cache-dir uv

# The venv lives outside /tests, so mounting the code over /tests does not hide it.
ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /tests
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

CMD ["pytest", "--version"]
