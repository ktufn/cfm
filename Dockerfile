# Базовый образ с Python
FROM python:3.12-slim

# Установим рабочую директорию внутри контейнера
WORKDIR /app

# Установим зависимости для psycopg2 (PostgreSQL driver)
RUN apt-get update && apt-get install -y gcc libpq-dev

# Скопируем файлы проекта
COPY requirements.txt .

# Установим зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё приложение внутрь контейнера
COPY . .

# Запускаем uvicorn при старте контейнера
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
