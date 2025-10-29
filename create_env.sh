#!/bin/bash

echo "🔑 Создание файла .env..."
echo ""

# Проверка, существует ли уже файл .env
if [ -f .env ]; then
    echo "⚠️  Файл .env уже существует!"
    read -p "Хотите перезаписать? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Отменено"
        exit 0
    fi
fi

# Запрос токена у пользователя
echo "Введите токен бота от @BotFather:"
read -r BOT_TOKEN

if [ -z "$BOT_TOKEN" ]; then
    echo "❌ Токен не может быть пустым!"
    exit 1
fi

# Создание файла .env
echo "BOT_TOKEN=$BOT_TOKEN" > .env

echo ""
echo "✅ Файл .env создан успешно!"
echo ""
echo "Теперь запустите бота:"
echo "./run.sh"
echo ""

