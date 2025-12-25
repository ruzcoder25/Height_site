 # Python version
FROM python:3.11-slim

# Ishchi papkani o'rnatish
WORKDIR /app

# Fayllarni nusxalash
COPY . /app

# Kutibxonalarni o'rnatish
RUN pip install --upgrade pip && pip install -r requirements.txt


# Portni ochish
EXPOSE 8000

# Container ishga tushganda Django serverni ishga tushurish
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

