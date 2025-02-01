FROM python:3.9-slim

# Устанавливаем необходимые зависимости, включая gcc и другие библиотеки
RUN apt-get update && apt-get install -y \
    pkg-config \
    libmariadb-dev \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt в контейнер
COPY requirements.txt /app/

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копируем все остальные файлы приложения
COPY . /app/

EXPOSE 8080

# Указываем команду для старта приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
