# Используем официальный Python-образ
FROM python:3.8-slim

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y libpq-dev gcc

# Создаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . /app

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт для сервера разработки
EXPOSE 8000

# Команда для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]