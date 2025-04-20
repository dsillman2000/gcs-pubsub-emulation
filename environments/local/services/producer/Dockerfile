FROM python:3.12-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends curl
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
WORKDIR /app
COPY . .
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root
ENV BOOTSTRAP_SERVERS=kafka:9092
CMD ["poetry", "run", "main"]
