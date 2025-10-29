#!/bin/bash

echo "🤖 Запуск Telegram бота..."
echo ""

# Проверка наличия виртуального окружения
if [ ! -d "venv" ]; then
    echo "⚠️  Виртуальное окружение не найдено!"
    echo "Запустите сначала: ./setup.sh"
    exit 1
fi

# Проверка наличия .env файла
if [ ! -f .env ]; then
    echo "⚠️  Файл .env не найден!"
    echo ""
    echo "Создайте файл .env и добавьте ваш токен:"
    echo "BOT_TOKEN=ваш_токен_от_BotFather"
    echo ""
    echo "Или выполните:"
    echo "echo 'BOT_TOKEN=ваш_токен' > .env"
    exit 1
fi

# Активация виртуального окружения
echo "🔄 Активирую виртуальное окружение..."
source venv/bin/activate

# Запуск бота
echo "🚀 Запускаю бота..."
echo ""
python bot.py

