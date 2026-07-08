# Etapa 1: builder (instala dependencias)

FROM python:3.12-slim as builder
WORKDIR /app
RUN pip install --no-cache-dir poetry==1.8.3
COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi --no-root

# Etapa 2: imagen final (ligera)

FROM python:3.12-slim
WORKDIR /app
ENV PYTHONPATH=/app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .
EXPOSE 8000
CMD ["sh", "-c", "alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port 8000"]
