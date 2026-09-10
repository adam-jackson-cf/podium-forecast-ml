FROM ghcr.io/astral-sh/uv:0.10.0@sha256:78a7ff97cd27b7124a5f3c2aefe146170793c56a1e03321dd31a289f6d82a04f AS uv
FROM python:3.12.12-slim-bookworm@sha256:593bd06efe90efa80dc4eee3948be7c0fde4134606dd40d8dd8dbcade98e669c
COPY --from=uv /uv /uvx /usr/local/bin/
WORKDIR /app
ENV UV_LINK_MODE=copy UV_COMPILE_BYTECODE=1
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project
COPY scripts/ scripts/
COPY tests/ tests/
COPY verification/ verification/
COPY src/ src/
RUN uv sync --frozen
USER 65532:65532
ENV HOME=/tmp UV_CACHE_DIR=/tmp/uv-cache
CMD ["uv", "run", "--no-sync", "pytest", "tests/seams", "-v", "-o", "cache_dir=/tmp/pytest-cache"]
