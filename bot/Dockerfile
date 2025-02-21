FROM python:3.8-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Устанавливаем зависимости для виртуального окружения
RUN apk update && apk add python3-dev \
                          gcc \
                          libc-dev \
                          libffi-dev \
                          bash

# Создаем виртуальное окружение и активируем его
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Обновляем pip и устанавливаем зависимости в виртуальном окружении
RUN pip install --upgrade pip
COPY req.txt ./
RUN pip install -r req.txt

COPY . /app

CMD ["python3", "main.py"]
