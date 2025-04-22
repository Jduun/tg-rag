FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi --without dev

COPY . /app

ENV PYTHONPATH="/app"

CMD ["python", "src/main.py"]