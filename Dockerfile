FROM python:3.11-slim

# Atrof-muhit o'zgaruvchilarini sozlash
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Ish katalogini yaratish
WORKDIR /app

# Sistema kutubxonalarini o'rnatish
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Python kutubxonalarini o'rnatish
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Loyiha fayllarini nusxalash
COPY . .

# Static fayllarni yig'ish uchun katalog yaratish
RUN mkdir -p /app/staticfiles /app/mediafiles

# Foydalanuvchi yaratish va ruxsatlar berish
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Gunicorn orqali ishga tushirish
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--threads", "2", "--timeout", "120", "config.wsgi:application"]