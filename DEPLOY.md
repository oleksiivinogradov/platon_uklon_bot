# 🚀 Развертывание бота на сервере (24/7 работа)

Чтобы бот работал постоянно без включенного компьютера, нужно развернуть его на сервере.

## 📋 Варианты развертывания

### ⭐ РЕКОМЕНДУЕМЫЕ БЕСПЛАТНЫЕ ВАРИАНТЫ:

1. **Railway.app** (рекомендуется) - 500 часов/месяц бесплатно
2. **Render.com** - бесплатный tier
3. **PythonAnywhere** - бесплатный аккаунт
4. **Fly.io** - бесплатный tier

### 💰 ПЛАТНЫЕ ВАРИАНТЫ:

5. **VPS (DigitalOcean, Linode)** - от $5/месяц
6. **Heroku** - от $7/месяц
7. **AWS/Google Cloud/Azure** - от $5/месяц

---

## 🎯 ВАРИАНТ 1: Railway.app (РЕКОМЕНДУЕТСЯ)

**Преимущества:**
- ✅ Бесплатно 500 часов/месяц
- ✅ Автоматический деплой из GitHub
- ✅ Очень простая настройка
- ✅ Логи в реальном времени

**Шаги:**

### 1. Подготовка проекта

Файлы уже готовы! Нужно только загрузить на GitHub.

### 2. Регистрация на Railway

1. Перейди на [railway.app](https://railway.app)
2. Нажми "Start a New Project"
3. Авторизуйся через GitHub
4. Выбери "Deploy from GitHub repo"
5. Выбери свой репозиторий `platon_uklon_bot`

### 3. Настройка переменных окружения

В Railway:
1. Открой свой проект
2. Перейди в "Variables"
3. Добавь переменную:
   ```
   BOT_TOKEN = твой_токен_от_BotFather
   ```

### 4. Деплой

Railway автоматически:
- Установит зависимости из `requirements.txt`
- Запустит `bot.py`
- Бот будет работать 24/7!

---

## 🎯 ВАРИАНТ 2: Render.com

**Преимущества:**
- ✅ Бесплатный tier
- ✅ Автодеплой из GitHub
- ✅ Простая настройка

**Шаги:**

1. Зарегистрируйся на [render.com](https://render.com)
2. Создай новый "Web Service"
3. Подключи GitHub репозиторий
4. Настройки:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python bot.py`
5. Добавь переменную окружения `BOT_TOKEN`
6. Нажми "Create Web Service"

---

## 🎯 ВАРИАНТ 3: PythonAnywhere

**Преимущества:**
- ✅ Полностью бесплатный
- ✅ Простой интерфейс
- ✅ Консоль в браузере

**Шаги:**

1. Зарегистрируйся на [pythonanywhere.com](https://www.pythonanywhere.com)
2. Открой Bash консоль
3. Клонируй репозиторий:
   ```bash
   git clone https://github.com/твой_юзернейм/platon_uklon_bot.git
   cd platon_uklon_bot
   ```
4. Создай виртуальное окружение:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
5. Создай файл `.env`:
   ```bash
   echo "BOT_TOKEN=твой_токен" > .env
   ```
6. Запусти бота:
   ```bash
   python bot.py
   ```
7. Для автозапуска: Перейди в "Tasks" → "Always-on task" → добавь команду запуска

---

## 🎯 ВАРИАНТ 4: VPS (Самый надежный)

**Рекомендую:** DigitalOcean, Linode, Vultr (~$5/месяц)

**Шаги:**

### 1. Создай сервер (Droplet)

1. Зарегистрируйся на DigitalOcean
2. Создай новый Droplet (Ubuntu 22.04)
3. Выбери минимальный план ($5/месяц)
4. Получи IP адрес

### 2. Подключись к серверу

```bash
ssh root@твой_ip_адрес
```

### 3. Установи зависимости

```bash
# Обновление системы
apt update && apt upgrade -y

# Установка Python и pip
apt install python3 python3-pip python3-venv git -y
```

### 4. Загрузи код бота

```bash
# Клонируй репозиторий
git clone https://github.com/твой_юзернейм/platon_uklon_bot.git
cd platon_uklon_bot

# Создай виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Установи зависимости
pip install -r requirements.txt
```

### 5. Настрой токен

```bash
echo "BOT_TOKEN=твой_токен_от_BotFather" > .env
```

### 6. Запусти бота в фоне (используй systemd)

Используй готовый файл `platon_bot.service` из проекта!

```bash
# Копируй service файл
sudo cp platon_bot.service /etc/systemd/system/

# Перезагрузи systemd
sudo systemctl daemon-reload

# Запусти бота
sudo systemctl start platon_bot

# Включи автозапуск
sudo systemctl enable platon_bot

# Проверь статус
sudo systemctl status platon_bot
```

### 7. Полезные команды

```bash
# Перезапустить бота
sudo systemctl restart platon_bot

# Остановить бота
sudo systemctl stop platon_bot

# Посмотреть логи
sudo journalctl -u platon_bot -f
```

---

## 🎯 ВАРИАНТ 5: Docker (Универсальный)

Используй готовый `Dockerfile` из проекта!

```bash
# Собрать образ
docker build -t platon_bot .

# Запустить контейнер
docker run -d --name platon_bot \
  -e BOT_TOKEN=твой_токен \
  --restart unless-stopped \
  platon_bot
```

---

## 🔧 Управление ботом на сервере

### Просмотр логов:
```bash
# Railway/Render - в веб-интерфейсе
# VPS с systemd:
sudo journalctl -u platon_bot -f

# Docker:
docker logs -f platon_bot
```

### Перезапуск:
```bash
# Railway/Render - через веб-интерфейс
# VPS:
sudo systemctl restart platon_bot

# Docker:
docker restart platon_bot
```

### Остановка:
```bash
# VPS:
sudo systemctl stop platon_bot

# Docker:
docker stop platon_bot
```

---

## 📊 Сравнение вариантов

| Вариант | Цена | Сложность | Надежность | Рекомендация |
|---------|------|-----------|------------|--------------|
| Railway | Бесплатно (500ч) | ⭐ Легко | ⭐⭐⭐ | ✅ Начинающим |
| Render | Бесплатно | ⭐⭐ Средне | ⭐⭐⭐ | ✅ Хорошо |
| PythonAnywhere | Бесплатно | ⭐ Легко | ⭐⭐ | Для тестов |
| VPS | $5/мес | ⭐⭐⭐ Сложно | ⭐⭐⭐⭐⭐ | ✅ Продакшен |
| Docker | Зависит | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Для опытных |

---

## ✅ Рекомендация для начинающих:

**Используй Railway.app:**

1. Загрузи код на GitHub
2. Подключи к Railway
3. Добавь BOT_TOKEN
4. Готово! Бот работает 24/7

**Время настройки: 5-10 минут**

---

## 🆘 Помощь

Если нужна помощь с настройкой:
1. Смотри файлы `railway.json`, `Dockerfile`, `platon_bot.service`
2. Они уже готовы в проекте!
3. Просто следуй инструкциям выше

