FROM python:3.14.0

# ARG VERSION=3.12

# FROM python:${VERSION}-slim

EXPOSE 8000

# VOLUME /data

RUN useradd -m myuser

USER myuser

LABEL version="2.1"
LABEL description="Task Manager API"

WORKDIR /app

ENV PYTONPATH=/app

ENV DATABASE_URL=sqlite:///.task.db

ENV APP_ENV=production

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app


ENTRYPOINT [ "uvicorn", "app.main:app" ]
CMD ["--host", "0.0.0.0", "--port", "8000"]