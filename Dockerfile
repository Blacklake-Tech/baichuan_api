FROM python:3.11-slim as builder

RUN apt-get update -yq && apt-get install -y \
  build-essential \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install poetry

RUN poetry export --format=requirements.txt --output=requirements.txt

FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /app/requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

COPY . /app/

CMD ["gunicorn", "baichuan_api.app:app", "--workers=4", "--worker-class=uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]
