FROM public.ecr.aws/docker/library/python:3.12.2-alpine AS base

FROM base AS deps

WORKDIR /app

RUN apk add build-base libffi-dev

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install --without=dev

FROM base AS runner

WORKDIR /app

ENV WORKERS=1 \
    PORT=8000 \
    APP_ENV=docker \
    VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=deps ${VIRTUAL_ENV} ${VIRTUAL_ENV}

ADD bootstrap.sh .
ADD src .

EXPOSE 8000

CMD ["sh", "bootstrap.sh"]
