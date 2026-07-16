#!/bin/bash

# Налаштування змінних (можеш змінювати за потреби)
IMAGE_NAME="flask-ai-app"
CONTAINER_NAME="my-flask-container"
PORT="5001"

echo "============================================="
echo "🚀 Починаємо процес деплою локального Docker..."
echo "============================================="

# 1. Перевірка, чи існує та запущений старий контейнер
if [ "$(docker ps -aq -f name=${CONTAINER_NAME})" ]; then
    echo "🧹 Знайдено старий контейнер '${CONTAINER_NAME}'. Зупиняємо та видаляємо..."
    docker rm -f ${CONTAINER_NAME}
fi

# 2. Збірка нового образу (використовуємо кеш для швидкості)
echo "📦 Збираємо новий Docker-образ '${IMAGE_NAME}'..."
docker build -t ${IMAGE_NAME} .

# Перевіряємо, чи успішно пройшла збірка
if [ $? -ne 0 ]; then
    echo "❌ Помилка під час збірки образу! Зупиняємо скрипт."
    exit 1
fi

# 3. Запуск нового контейнера
echo "🏃 Запускаємо новий контейнер '${CONTAINER_NAME}' на порту ${PORT}..."
docker run -d \
  -p ${PORT}:${PORT} \
  --add-host=host.docker.internal:host-gateway \
  --name ${CONTAINER_NAME} \
  ${IMAGE_NAME}

# Перевіряємо статус запуску
if [ $? -eq 0 ]; then
    echo "============================================="
    echo "🎉 Контейнер успішно запущено у фоні!"
    echo "🌐 Додаток доступний за адресою: http://localhost:${PORT}"
    echo "📊 Для перегляду логів виконай: docker logs -f ${CONTAINER_NAME}"
    echo "============================================="
else
    echo "❌ Не вдалося запустити контейнер."
    exit 1
fi