FROM public.ecr.aws/docker/library/python:3.11-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_NO_CACHE=1
ENV UV_COMPILE_BYTECODE=1

# Allow overriding package version based on Git repository state without installing git
# in the image.
ARG SETUPTOOLS_SCM_PRETEND_VERSION

WORKDIR /app
COPY . .
RUN uv sync
ENV PATH="/app/.venv/bin:$PATH"

CMD ["lgfk-cli"]
