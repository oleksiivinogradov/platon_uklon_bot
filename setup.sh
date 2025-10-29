#!/bin/bash

echo "🔧 Настройка Telegram бота..."
echo ""

# Проверка наличия Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 не установлен!"
    echo "Установите через: brew install python3"
    exit 1
fi

# Исправление SSL сертификатов (проблема macOS)
echo "🔐 Проверяю SSL сертификаты..."
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
SSL_CERT_SCRIPT="/Applications/Python ${PYTHON_VERSION}/Install Certificates.command"
if [ -f "$SSL_CERT_SCRIPT" ]; then
    echo "📦 Устанавливаю SSL сертификаты для Python..."
    bash "$SSL_CERT_SCRIPT" || true
fi

# Создание виртуального окружения
if [ ! -d "venv" ]; then
    echo "📦 Создаю виртуальное окружение..."
    python3 -m venv venv
    echo "✅ Виртуальное окружение создано"
else
    echo "✅ Виртуальное окружение уже существует"
fi

# Активация виртуального окружения
echo "🔄 Активирую виртуальное окружение..."
source venv/bin/activate

# Обновление pip (игнорируем ошибки SSL)
echo "📦 Обновляю pip..."
pip install --upgrade pip --trusted-host pypi.org --trusted-host files.pythonhosted.org 2>/dev/null || true

# Установка зависимостей (с обходом проблемы SSL)
echo "📦 Устанавливаю зависимости..."
if ! pip install -r requirements.txt 2>/dev/null; then
    echo "⚠️  Пробую альтернативный способ установки..."
    pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org python-telegram-bot python-dotenv
fi

# Проверка установки
if python -c "import telegram" 2>/dev/null; then
    echo ""
    echo "✅ Установка завершена успешно!"
else
    echo ""
    echo "⚠️  Возможны проблемы с установкой."
    echo "Попробуйте запустить вручную:"
    echo "source venv/bin/activate"
    echo "pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org python-telegram-bot python-dotenv"
fi

echo ""
echo "📝 Следующие шаги:"
echo "1. Создайте бота в Telegram через @BotFather"
echo "2. Получите токен бота"
echo "3. Создайте файл .env и добавьте: BOT_TOKEN=ваш_токен"
echo "4. Запустите бота командой: ./run.sh"
echo ""

