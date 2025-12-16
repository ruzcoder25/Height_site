## Django uchun Dockerfile
#FROM python:3.11-slim
#
## Ishchi papkani o‘rnatish
#WORKDIR /app
#
## Faqat requirements faylini avval nusxalash
## (Docker cache’ni ishlatish uchun)
#COPY requirements.txt .
#
## Pip upgrade va kutubxonalarni o‘rnatish
#RUN pip install --upgrade pip \
#    && pip install -r requirements.txt
#
## Loyiha fayllarini nusxalash
#COPY . .
#
## Statik fayllarni tayyorlash (agar kerak bo‘lsa)
## RUN python manage.py collectstatic --noinput
#
## Port ochish
#EXPOSE 8000
#
## Django serverni ishga tushirish
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# System dependencies (pandas, psycopg2 uchun)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && apt-get clean

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# static yig‘ish (production uchun)
RUN python manage.py collectstatic --noinput || true
