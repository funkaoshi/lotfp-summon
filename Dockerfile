FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY . /app

RUN [ "pip", "install", "-r", "requirements.txt" ]

EXPOSE 8001

CMD [ "gunicorn", "-w", "4", "--bind", "0.0.0.0:8001", "summon:app"]

