FROM python:3.11-alpine

# Устанавливаем рабочую директорию в контейнере
WORKDIR /usr/src/app

# Копируем файл зависимостей и устанавливаем их
COPY req.txt ./

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r req.txt

# Копируем исходный код проекта
COPY .. .

# Собираем статические файлы

RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Устанавливаем Nginx

# Копируем конфигурацию Nginx



# Открываем порт 80
EXPOSE 80
EXPOSE 8003

#nginx &&

# Запускаем Nginx и Gunicorn
CMD ["sh", "-c", " exec gunicorn app.wsgi:application --bind 0.0.0.0:8003"]


