FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir poetry


COPY pyproject.toml poetry.lock ./


RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction --no-ansi


COPY . .

ENV ENV_FILE=.env

# Устанавливает переменную окружения, которая гарантирует, что вывод из python будет отправлен прямо в терминал без предварительной буферизации
ENV PYTHONUNBUFFERED 1


EXPOSE 8000


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
