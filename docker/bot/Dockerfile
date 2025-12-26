FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential \
    && rm -rf /var/lib/apt/lists/*

# requirements
COPY backend/requirements.txt /app/requirements.txt

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# bot package ni nusxalash
COPY bot /app/bot

# MUHIM: Python bot ni package sifatida ko‘rsin
ENV PYTHONPATH=/app

# MUHIM: script emas, MODULE sifatida ishga tushiramiz
CMD ["python", "-m", "bot.main"]
