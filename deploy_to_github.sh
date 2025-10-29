#!/bin/bash

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║       🚀 ЗАГРУЗКА БОТА НА GITHUB ДЛЯ ДЕПЛОЯ 🚀          ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Проверка Git
if ! command -v git &> /dev/null; then
    echo "❌ Git не установлен!"
    echo "Установи: brew install git"
    exit 1
fi

# Инициализация Git (если еще не сделано)
if [ ! -d ".git" ]; then
    echo "📦 Инициализирую Git репозиторий..."
    git init
    echo "✅ Git инициализирован"
else
    echo "✅ Git репозиторий уже существует"
fi

# Добавляем все файлы
echo "📝 Добавляю файлы..."
git add .

# Создаем коммит
echo "💾 Создаю коммит..."
git commit -m "Sigma Bot v2.6.0 - Full version with 12 languages, video download, AI features"

echo ""
echo "✅ Файлы готовы к загрузке!"
echo ""
echo "📋 СЛЕДУЮЩИЕ ШАГИ:"
echo ""
echo "1. Создай репозиторий на GitHub.com:"
echo "   → Открой https://github.com/new"
echo "   → Название: platon_uklon_bot"
echo "   → Описание: Telegram Sigma Bot with AI features"
echo "   → Public или Private (на твой выбор)"
echo "   → НЕ добавляй README, .gitignore (уже есть!)"
echo "   → Create repository"
echo ""
echo "2. Скопируй команды которые GitHub покажет:"
echo "   → «…or push an existing repository from the command line»"
echo ""
echo "3. Или выполни эти команды (замени USERNAME):"
echo ""
echo "   git remote add origin https://github.com/USERNAME/platon_uklon_bot.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "4. После загрузки на GitHub:"
echo "   → Читай QUICK_DEPLOY.md для деплоя на Railway"
echo "   → Или DEPLOY.md для других вариантов"
echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║  ✅ Git готов! Создай репозиторий и залей код!           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

