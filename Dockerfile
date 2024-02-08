FROM python:3.10-alpine

EXPOSE 8000

WORKDIR /app

RUN pip install --upgrade pip
RUN apk add gcc musl-dev libffi-dev openssl-dev
RUN pip install poetry

COPY . /app

RUN poetry config virtualenvs.create false  \
    && poetry install --no-interaction --no-ansi --without test

CMD ["poetry", "run", "uvicorn", "logger_fastapi.main:app", "--host", "0.0.0.0", "--port", "8000"]
