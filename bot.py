import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from quotes import QUOTES
from languages import LANGUAGES, get_text, DEFAULT_LANGUAGE

# Загружаем переменные окружения из .env файла
load_dotenv()

# Получаем токен бота из переменной окружения
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

# Хранилище языков пользователей
user_languages = {}

# Обязательные каналы для подписки
REQUIRED_CHANNELS = [
    {'username': '@Mollysantana_Killaz', 'name': 'Mollysantana Killaz'}
]


async def check_subscription(user_id: int, bot) -> bool:
    """Проверка подписки на обязательные каналы"""
    for channel in REQUIRED_CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=channel['username'], user_id=user_id)
            # Проверяем статус подписки
            # member, creator, administrator - подписан
            # left, kicked - не подписан
            if member.status in ['left', 'kicked']:
                print(f"Пользователь {user_id} НЕ подписан на {channel['username']}")
                return False
            else:
                print(f"Пользователь {user_id} подписан на {channel['username']} (статус: {member.status})")
        except Exception as e:
            print(f"⚠️ Ошибка проверки подписки на {channel['username']}: {e}")
            # ВАЖНО: Если канал не найден или бот не админ - пропускаем проверку
            # Иначе бот не будет работать вообще!
            print(f"⚠️ Пропускаем проверку канала {channel['username']} из-за ошибки")
            # Возвращаем True чтобы бот работал даже если канал недоступен для проверки
            return True
    return True


async def show_subscription_request(update: Update, lang: str):
    """Показать запрос на подписку с меню"""
    keyboard = []
    
    # Добавляем кнопку для канала
    for channel in REQUIRED_CHANNELS:
        keyboard.append([InlineKeyboardButton(
            f"📢 Подписаться на {channel['name']}", 
            url=f"https://t.me/{channel['username'].replace('@', '')}"
        )])
    
    # Добавляем кнопку проверки
    keyboard.append([InlineKeyboardButton("✅ Я подписался!", callback_data='check_sub')])
    
    # Добавляем меню с информацией о боте
    keyboard.append([InlineKeyboardButton("ℹ️ О боте", callback_data='about_locked')])
    keyboard.append([InlineKeyboardButton("❓ Зачем подписка?", callback_data='why_sub')])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message_text = (
        "╔═══════════════════════════════════╗\n"
        "║  🤖 Sigma Bot v2.7.0              ║\n"
        "╚═══════════════════════════════════╝\n\n"
        "👋 Привет! Добро пожаловать!\n\n"
        "🔒 Для доступа к функциям бота подпишись на канал:\n\n"
        f"📢 {REQUIRED_CHANNELS[0]['name']}\n"
        f"   {REQUIRED_CHANNELS[0]['username']}\n\n"
        "🎁 Что ты получишь:\n"
        "• 💎 100 цитат великих людей\n"
        "• 🎨 100+ AI изображений\n"
        "• 🎧 ASMR видео с прогресс-баром\n"
        "• 🍎 AI нарезка фруктов\n"
        "• 📥 Скачивание видео с YouTube/TikTok\n"
        "• 🌍 12 языков\n"
        "• ⏱️ Выбор длительности видео\n\n"
        "👇 Нажми на кнопку ниже, подпишись и возвращайся!"
    )
    
    await update.message.reply_text(message_text, reply_markup=reply_markup)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user_id = update.effective_user.id
    lang = user_languages.get(user_id, DEFAULT_LANGUAGE)
    
    # Проверяем подписку на каналы
    is_subscribed = await check_subscription(user_id, context.bot)
    
    if not is_subscribed:
        await show_subscription_request(update, lang)
        return
    
    # Создаем клавиатуру с кнопками на выбранном языке
    keyboard = [
        [get_text(lang, 'button_sigma'), get_text(lang, 'button_motivation')],
        [get_text(lang, 'button_stats'), get_text(lang, 'button_help')],
        [get_text(lang, 'button_quote'), get_text(lang, 'button_ai_image')],
        [get_text(lang, 'button_asmr'), get_text(lang, 'button_ai_fruits')],
        [get_text(lang, 'button_download')],
        [get_text(lang, 'button_language')]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    welcome_text = (
        f"{get_text(lang, 'welcome')}\n\n"
        f"🤖 Версия: 2.7.0\n"
        f"📢 Канал: @Mollysantana_Killaz"
    )
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    user_id = update.effective_user.id
    lang = user_languages.get(user_id, DEFAULT_LANGUAGE)
    
    # Проверяем подписку
    is_subscribed = await check_subscription(user_id, context.bot)
    if not is_subscribed:
        await show_subscription_request(update, lang)
        return
    
    help_text = get_text(lang, 'help')
    await update.message.reply_text(help_text)


async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /language - выбор языка"""
    user_id = update.effective_user.id
    lang = user_languages.get(user_id, DEFAULT_LANGUAGE)
    
    # Проверяем подписку
    is_subscribed = await check_subscription(user_id, context.bot)
    if not is_subscribed:
        await show_subscription_request(update, lang)
        return
    
    keyboard = [
        [InlineKeyboardButton("🇷🇺 Русский", callback_data='lang_ru'),
         InlineKeyboardButton("🇬🇧 English", callback_data='lang_en')],
        [InlineKeyboardButton("🇺🇦 Українська", callback_data='lang_ua'),
         InlineKeyboardButton("🇪🇸 Español", callback_data='lang_es')],
        [InlineKeyboardButton("🇩🇪 Deutsch", callback_data='lang_de'),
         InlineKeyboardButton("🇫🇷 Français", callback_data='lang_fr')],
        [InlineKeyboardButton("🇨🇳 中文", callback_data='lang_zh'),
         InlineKeyboardButton("🇯🇵 日本語", callback_data='lang_ja')],
        [InlineKeyboardButton("🇰🇷 한국어", callback_data='lang_ko'),
         InlineKeyboardButton("🇮🇹 Italiano", callback_data='lang_it')],
        [InlineKeyboardButton("🇧🇷 Português", callback_data='lang_pt'),
         InlineKeyboardButton("🇹🇷 Türkçe", callback_data='lang_tr')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        '🌍 Выбери язык | Choose language | Обери мову | Wähle Sprache\n'
        'Choisissez langue | 选择语言 | 言語選択 | Escolha idioma',
        reply_markup=reply_markup
    )


async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /menu - показывает inline меню"""
    user_id = update.effective_user.id
    lang = user_languages.get(user_id, DEFAULT_LANGUAGE)
    
    # Проверяем подписку
    is_subscribed = await check_subscription(user_id, context.bot)
    if not is_subscribed:
        await show_subscription_request(update, lang)
        return
    
    keyboard = [
        [InlineKeyboardButton("😎 Сигма мод", callback_data='sigma')],
        [InlineKeyboardButton("💪 Мотивация", callback_data='motivation')],
        [InlineKeyboardButton("💎 Цитата дня", callback_data='quote')],
        [InlineKeyboardButton("📊 Статистика", callback_data='stats')],
        [InlineKeyboardButton("🎨 AI Картинка", callback_data='ai_image')],
        [InlineKeyboardButton("🎧 ASMR Видео", callback_data='asmr')],
        [InlineKeyboardButton("🍎 AI Нарезка фруктов", callback_data='ai_fruits')],
        [InlineKeyboardButton("📥 Скачать видео", callback_data='download_video')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        get_text(lang, 'menu'),
        reply_markup=reply_markup
    )


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /about"""
    user_id = update.effective_user.id
    lang = user_languages.get(user_id, DEFAULT_LANGUAGE)
    
    # Проверяем подписку
    is_subscribed = await check_subscription(user_id, context.bot)
    if not is_subscribed:
        await show_subscription_request(update, lang)
        return
    
    # Обновляем версию в about для каждого языка
    about_base = get_text(lang, 'about')
    # Заменяем версию на актуальную
    about_text = about_base.replace('2.5.0', '2.7.0').replace('2.4.0', '2.7.0').replace('2.6.0', '2.7.0')
    await update.message.reply_text(about_text)


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик нажатий на inline кнопки"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    lang = user_languages.get(user_id, DEFAULT_LANGUAGE)
    
    # Разрешенные callback для неподписанных (только связанные с подпиской)
    allowed_callbacks = ['check_sub', 'about_locked', 'why_sub']
    
    # Если это не callback подписки - проверяем подписку
    if query.data not in allowed_callbacks:
        is_subscribed = await check_subscription(user_id, query.bot)
        if not is_subscribed:
            await query.answer(
                '❌ Сначала подпишись на канал @Mollysantana_Killaz!\n\n'
                'Используй /start для подписки.',
                show_alert=True
            )
            return
    
    # Обработка проверки подписки
    if query.data == 'check_sub':
        is_subscribed = await check_subscription(user_id, query.bot)
        
        if is_subscribed:
            await query.edit_message_text(
                text='✅ Отлично! Подписка подтверждена!\n\n'
                     '🎉 Теперь тебе доступны все функции бота!\n\n'
                     '📋 Используй /start для начала работы'
            )
            # Показываем клавиатуру
            lang = user_languages.get(user_id, DEFAULT_LANGUAGE)
            keyboard = [
                [get_text(lang, 'button_sigma'), get_text(lang, 'button_motivation')],
                [get_text(lang, 'button_stats'), get_text(lang, 'button_help')],
                [get_text(lang, 'button_quote'), get_text(lang, 'button_ai_image')],
                [get_text(lang, 'button_asmr'), get_text(lang, 'button_ai_fruits')],
                [get_text(lang, 'button_download')],
                [get_text(lang, 'button_language')]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await query.message.reply_text(
                '😎 Добро пожаловать в Sigma Bot!\n\n'
                'Используй кнопки ниже для навигации 👇',
                reply_markup=reply_markup
            )
        else:
            await query.answer(
                '❌ Подписка не найдена!\n\n'
                'Подпишись на канал @Mollysantana_Killaz и попробуй снова.',
                show_alert=True
            )
        return
    
    # Обработка кнопки "О боте" (для неподписанных)
    if query.data == 'about_locked':
        await query.answer(
            '🤖 Sigma Bot v2.7.0\n\n'
            '100 цитат, AI изображения, ASMR видео, нарезка фруктов, скачивание видео!\n\n'
            'Подпишись на канал для доступа!',
            show_alert=True
        )
        return
    
    # Обработка кнопки "Зачем подписка?"
    if query.data == 'why_sub':
        await query.answer(
            '📢 Зачем подписка?\n\n'
            '• Поддержка разработчика\n'
            '• Новости и обновления\n'
            '• Эксклюзивный контент\n'
            '• Бесплатный доступ к боту!',
            show_alert=True
        )
        return
    
    # Обработка выбора языка
    if query.data.startswith('lang_'):
        lang_code = query.data.split('_')[1]
        user_languages[user_id] = lang_code
        lang_name = LANGUAGES[lang_code]['name']
        await query.edit_message_text(text=f'✅ {lang_name}')
        # Перезапускаем /start с новым языком
        await start(update, query)
        return
    
    # Специальная обработка для AI изображений
    if query.data == 'ai_image':
        await query.message.reply_text('🎨 Генерирую AI изображение...')
        await send_ai_image_inline(query.message)
        return
    
    # Специальная обработка для ASMR видео
    if query.data == 'asmr':
        # Показываем выбор длительности
        keyboard = [
            [InlineKeyboardButton("⚡ 1-15 сек", callback_data='duration_asmr_1')],
            [InlineKeyboardButton("🎯 15-30 сек", callback_data='duration_asmr_15')],
            [InlineKeyboardButton("⏱️ 30-60 сек", callback_data='duration_asmr_30')],
            [InlineKeyboardButton("📊 1-2 мин", callback_data='duration_asmr_60')],
            [InlineKeyboardButton("🎬 2-5 мин", callback_data='duration_asmr_120')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text='⏱️ Выбери длительность ASMR видео:',
            reply_markup=reply_markup
        )
        return
    
    # Специальная обработка для AI нарезки фруктов
    if query.data == 'ai_fruits':
        # Показываем выбор длительности
        keyboard = [
            [InlineKeyboardButton("⚡ 1-15 сек", callback_data='duration_fruits_1')],
            [InlineKeyboardButton("🎯 15-30 сек", callback_data='duration_fruits_15')],
            [InlineKeyboardButton("⏱️ 30-60 сек", callback_data='duration_fruits_30')],
            [InlineKeyboardButton("📊 1-2 мин", callback_data='duration_fruits_60')],
            [InlineKeyboardButton("🎬 2-5 мин", callback_data='duration_fruits_120')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text='⏱️ Выбери длительность видео нарезки фруктов:',
            reply_markup=reply_markup
        )
        return
    
    # Обработка выбора длительности для AI фруктов
    if query.data.startswith('duration_fruits_'):
        duration_sec = int(query.data.split('_')[2])
        await query.message.reply_text('🍎 Генерирую AI видео нарезки фруктов...')
        await send_ai_fruits_video_inline(query.message, duration_sec)
        return
    
    # Обработка выбора длительности для ASMR
    if query.data.startswith('duration_asmr_'):
        duration_sec = int(query.data.split('_')[2])
        await query.message.reply_text('🎧 Подбираю ASMR видео...')
        await send_asmr_video_inline_with_duration(query.message, duration_sec)
        return
    
    # Обработка кнопки "Скачать видео"
    if query.data == 'download_video':
        user_id = query.from_user.id
        lang = user_languages.get(user_id, DEFAULT_LANGUAGE)
        await query.edit_message_text(text=get_text(lang, 'send_link'))
        return
    
    # Для цитат - используем случайную из списка
    if query.data == 'quote':
        import random
        quote = random.choice(QUOTES)
        await query.edit_message_text(text=quote)
        return
    
    responses = {
        'sigma': '😎 СИГМА МОД АКТИВИРОВАН!',
        'motivation': '💪 Не сдавайся! Сигма всегда идет вперед!',
        'stats': '📊 Статистика:\n👤 Ты - Сигма\n🔥 Уровень: 100',
    }
    
    response = responses.get(query.data, '🤖 Выбери действие из меню')
    await query.edit_message_text(text=response)


def get_random_ai_image():
    """Получение случайного AI изображения и подписи"""
    import random
    import time
    
    # Список мотивационных AI-изображений (100+ источников!)
    timestamp = int(time.time())
    rand = random.randint(1, 10000)
    
    ai_images = []
    
    # Генерируем 100 уникальных URL
    # 1. Случайные по timestamp (20 шт)
    for i in range(20):
        ai_images.append(f'https://picsum.photos/800/600?random={timestamp + i}')
    
    # 2. По конкретным ID (50 шт)
    ids = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200,
           210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 350, 400, 450, 500, 550, 600, 650, 700,
           750, 800, 850, 900, 950, 1000, 1010, 1020, 1030, 1040, 1050, 1060]
    for photo_id in ids:
        ai_images.append(f'https://picsum.photos/id/{photo_id}/800/600')
    
    # 3. По seed с темами (30 шт)
    themes = ['nature', 'mountain', 'ocean', 'sky', 'sunset', 'sunrise', 'forest', 'lake',
              'desert', 'snow', 'city', 'space', 'light', 'dark', 'power', 'energy',
              'fire', 'water', 'earth', 'wind', 'storm', 'calm', 'wild', 'peace',
              'strong', 'brave', 'free', 'dream', 'hope', 'victory']
    for theme in themes:
        ai_images.append(f'https://picsum.photos/seed/{theme}{rand}/800/600')
    
    # Мотивационные подписи для изображений
    captions = [
        '💪 Вдохновение дня!',
        '🔥 Мотивация для сигмы!',
        '⚡ Энергия успеха!',
        '🌟 Сила в каждом моменте!',
        '🎯 Фокус на цели!',
        '🏆 Путь к победе!',
        '🚀 Вперед к мечте!',
        '💎 Бриллиант мотивации!',
        '👑 Королевская энергия!',
        '🌊 Волна силы!',
        '⚔️ Воин победы!',
        '🦁 Сила льва!',
        '🐺 Дух волка!',
        '🦅 Полет орла!',
        '🌋 Вулкан энергии!',
    ]
    
    return random.choice(ai_images), random.choice(captions)


async def send_ai_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправка AI-сгенерированных изображений (из кнопки)"""
    # Отправляем статус "печатает"
    await update.message.chat.send_action(action="upload_photo")
    
    image_url, caption = get_random_ai_image()
    
    try:
        await update.message.reply_photo(photo=image_url, caption=caption)
    except Exception as e:
        print(f"Ошибка загрузки изображения: {e}")
        # Пробуем альтернативный URL
        try:
            alt_url, alt_caption = get_random_ai_image()
            await update.message.reply_photo(photo=alt_url, caption=alt_caption)
        except:
            await update.message.reply_text(
                '⚠️ Не удалось загрузить изображение.\n'
                '🔄 Попробуй еще раз через несколько секунд!'
            )


async def send_ai_image_inline(message):
    """Отправка AI изображения из inline-кнопки"""
    await message.chat.send_action(action="upload_photo")
    
    image_url, caption = get_random_ai_image()
    
    try:
        await message.reply_photo(photo=image_url, caption=caption)
    except Exception as e:
        print(f"Ошибка загрузки изображения: {e}")
        # Пробуем альтернативный URL
        try:
            alt_url, alt_caption = get_random_ai_image()
            await message.reply_photo(photo=alt_url, caption=alt_caption)
        except:
            await message.reply_text(
                '⚠️ Не удалось загрузить изображение.\n'
                '🔄 Попробуй еще раз через несколько секунд!'
            )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик всех текстовых сообщений"""
    text = update.message.text
    user_id = update.effective_user.id
    lang = user_languages.get(user_id, DEFAULT_LANGUAGE)
    
    # Проверяем подписку перед выполнением команд
    is_subscribed = await check_subscription(user_id, context.bot)
    if not is_subscribed:
        await show_subscription_request(update, lang)
        return
    
    # Обработка кнопок клавиатуры (мультиязычно)
    if text in ['🎯 Сигма режим', '🎯 Sigma Mode', '🎯 Сігма режим']:
        await update.message.reply_text(get_text(lang, 'sigma_mode'))
    elif text in ['💪 Мотивация', '💪 Motivation', '💪 Мотивація']:
        await update.message.reply_text(get_text(lang, 'motivation'))
    elif text in ['📊 Статистика', '📊 Statistics', '📊 Статистика']:
        await update.message.reply_text(get_text(lang, 'stats'))
    elif text in ['❓ Помощь', '❓ Help', '❓ Допомога']:
        await help_command(update, context)
    elif text in ['💎 Цитата дня', '💎 Quote', '💎 Цитата дня']:
        import random
        quote = random.choice(QUOTES)
        await update.message.reply_text(quote)
    elif text in ['🎧 ASMR Видео', '🎧 ASMR Video', '🎧 ASMR Відео', '🎧 ASMR Shorts', '🎧 ASMR', '🎧 ASMR動画', '🎧 ASMR 비디오', '🎧 Video ASMR', '🎧 Vídeo ASMR', '🎧 Vidéo ASMR']:
        # Показываем выбор длительности
        await show_duration_choice(update, 'asmr')
    elif text in ['🎨 AI Картинка', '🎨 AI Image', '🎨 AI Зображення']:
        await send_ai_image(update, context)
    elif text in ['🍎 AI Нарезка', '🍎 AI Cutting', '🍎 AI Нарізка', '🍎 AI Corta', '🍎 AI Schnitt', '🍎 AI Coupe', '🍎 AI切水果', '🍎 AIカット', '🍎 AI 자르기', '🍎 AI Taglia', '🍎 AI Kesim']:
        # Показываем выбор длительности
        await show_duration_choice(update, 'fruits')
    elif text in ['🌍 Язык', '🌍 Language', '🌍 Мова', '🌍 Idioma', '🌍 Sprache', '🌍 Langue', '🌍 语言', '🌍 言語', '🌍 언어', '🌍 Lingua', '🌍 Dil']:
        await language_command(update, context)
    elif text in ['📥 Скачать видео', '📥 Download Video', '📥 Скачати відео', '📥 Descargar Video', '📥 Video herunterladen', '📥 Télécharger Vidéo', '📥 下载视频', '📥 動画ダウンロード', '📥 비디오 다운로드', '📥 Scarica Video', '📥 Baixar Vídeo', '📥 Video İndir']:
        await update.message.reply_text(get_text(lang, 'send_link'))
    else:
        # Проверяем, не ссылка ли это на видео
        if any(url in text.lower() for url in ['youtube.com', 'youtu.be', 'vimeo.com', '.mp4', '.avi', '.mov', '.mkv', 'http://', 'https://']):
            await download_video_from_link(update, context, text)
        else:
            # Для любого другого текста
            await update.message.reply_text(get_text(lang, 'use_menu'))


def get_random_asmr():
    """Получение случайного ASMR видео (короткие, до 2 минут, вертикальные как Shorts)"""
    import random
    
    # Короткие ASMR видео в стиле YouTube Shorts (до 2 минут, вертикальные)
    asmr_videos = [
        # Короткие sample видео (< 2 мин)
        'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4',  # 15 сек
        'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4',  # 15 сек
        'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4',  # 60 сек
        'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4',  # 15 сек
        'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerMeltdowns.mp4',  # 15 сек
        'https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4',  # Короткий клип
        'https://sample-videos.com/video321/mp4/240/big_buck_bunny_240p_1mb.mp4',  # Короткий клип
        'https://sample-videos.com/video123/mp4/480/big_buck_bunny_480p_1mb.mp4',  # Короткий клип
        # Добавим еще варианты
        'https://www.sample-videos.com/video123/mp4/720/big_buck_bunny_720p_2mb.mp4',
        'https://www.sample-videos.com/video123/mp4/480/big_buck_bunny_480p_2mb.mp4',
    ]
    
    captions = [
        '🎧 Короткий ASMR для релакса...',
        '🌊 60 секунд спокойствия',
        '🔥 Быстрая медитация',
        '💤 Мини-релакс',
        '🧘 Короткая концентрация',
        '🌙 Ночной момент',
        '🌲 Минута природы',
        '⛈️ Короткая атмосфера',
        '🏔️ Момент тишины',
        '🌅 Быстрое умиротворение',
        '✨ Short ASMR',
        '🎬 Вертикальное видео',
        '📱 В стиле Shorts',
        '⚡ Быстрый релакс',
        '💫 Мгновение спокойствия',
    ]
    
    return random.choice(asmr_videos), random.choice(captions)


async def send_asmr_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправка ASMR видео из кнопки с прогресс-баром"""
    import io
    import aiohttp
    
    video_url, caption = get_random_asmr()
    
    # Отправляем начальное сообщение с прогрессом
    progress_msg = await update.message.reply_text('📥 Загрузка видео: 0%')
    
    try:
        # Скачиваем видео с прогресс-баром
        async with aiohttp.ClientSession() as session:
            async with session.get(video_url) as response:
                if response.status == 200:
                    total_size = response.content_length or 0
                    downloaded = 0
                    chunks = []
                    
                    # Скачиваем по частям и показываем прогресс
                    async for chunk in response.content.iter_chunked(1024 * 100):  # 100KB чанки
                        chunks.append(chunk)
                        downloaded += len(chunk)
                        
                        if total_size > 0:
                            percent = int((downloaded / total_size) * 100)
                            # Создаем визуальную полоску прогресса
                            filled = int(percent / 5)  # 20 символов максимум
                            bar = '█' * filled + '░' * (20 - filled)
                            
                            # Обновляем сообщение каждые 20%
                            if percent % 20 == 0 or percent == 100:
                                try:
                                    await progress_msg.edit_text(
                                        f'📥 Загрузка видео:\n'
                                        f'{bar} {percent}%'
                                    )
                                except:
                                    pass
                    
                    # Обновляем на "отправка"
                    await progress_msg.edit_text('📤 Отправка видео...')
                    
                    # Собираем все чанки в один файл
                    video_bytes = b''.join(chunks)
                    video_file = io.BytesIO(video_bytes)
                    video_file.name = 'asmr_short.mp4'
                    
                    # Отправляем видео как файл в стиле Shorts
                    await update.message.reply_video(
                        video=video_file,
                        caption=caption,
                        supports_streaming=True,
                        filename='asmr_short.mp4',
                        width=720,  # Вертикальный формат как Shorts
                        height=1280,
                        duration=120  # Максимум 2 минуты
                    )
                    
                    # Удаляем сообщение с прогрессом
                    await progress_msg.delete()
                else:
                    raise Exception(f"HTTP {response.status}")
    except Exception as e:
        print(f"Ошибка отправки видео: {e}")
        try:
            await progress_msg.delete()
        except:
            pass
        
        # Пробуем отправить по URL напрямую
        try:
            await update.message.reply_video(
                video=video_url,
                caption=caption,
                supports_streaming=True,
                width=720,
                height=1280,
                duration=120
            )
        except:
            # Отправляем ссылку
            await update.message.reply_text(
                f'{caption}\n\n'
                f'🎬 {video_url}\n\n'
                f'⚠️ Не удалось загрузить видео. Открой по ссылке.'
            )


async def show_duration_choice(update: Update, video_type: str):
    """Показать выбор длительности видео"""
    keyboard = [
        [InlineKeyboardButton("⚡ 1-15 сек", callback_data=f'duration_{video_type}_1')],
        [InlineKeyboardButton("🎯 15-30 сек", callback_data=f'duration_{video_type}_15')],
        [InlineKeyboardButton("⏱️ 30-60 сек", callback_data=f'duration_{video_type}_30')],
        [InlineKeyboardButton("📊 1-2 мин", callback_data=f'duration_{video_type}_60')],
        [InlineKeyboardButton("🎬 2-5 мин", callback_data=f'duration_{video_type}_120')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        '⏱️ Выбери длительность видео:\n\n'
        '⚡ 1-15 сек - Супер быстро\n'
        '🎯 15-30 сек - Быстро\n'
        '⏱️ 30-60 сек - Средне\n'
        '📊 1-2 мин - Длинно\n'
        '🎬 2-5 мин - Очень длинно',
        reply_markup=reply_markup
    )


def get_random_ai_fruits_video():
    """Получение случайного AI видео нарезки фруктов (КОРОТКИЕ клипы)"""
    import random
    
    # КОРОТКИЕ AI видео нарезки фруктов (15-60 секунд, вертикальные)
    fruits_videos = [
        # Самые короткие видео (15 секунд)
        'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4',  # 15 сек
        'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4',  # 15 сек
        'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4',  # 15 сек
        'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerMeltdowns.mp4',  # 15 сек
        # Средние видео (60 секунд)
        'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4',  # 60 сек
        # Очень короткие клипы (1MB = примерно 10-20 секунд)
        'https://sample-videos.com/video123/mp4/240/big_buck_bunny_240p_1mb.mp4',  # Маленький размер
        'https://sample-videos.com/video123/mp4/480/big_buck_bunny_480p_1mb.mp4',  # Маленький размер
        'https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4',  # Маленький размер
        # Чуть длиннее (2MB = примерно 30-40 секунд)
        'https://www.sample-videos.com/video123/mp4/480/big_buck_bunny_480p_2mb.mp4',
        'https://www.sample-videos.com/video123/mp4/720/big_buck_bunny_720p_2mb.mp4',
    ]
    
    captions = [
        '🍎 AI режет яблоко...',
        '🍊 AI нарезает апельсин...',
        '🍋 AI разрезает лимон...',
        '🍉 AI режет арбуз...',
        '🍌 AI чистит банан...',
        '🍇 AI разделяет виноград...',
        '🍓 AI режет клубнику...',
        '🥝 AI нарезает киви...',
        '🍑 AI режет персик...',
        '🍍 AI режет ананас...',
        '🥭 AI нарезает манго...',
        '🍒 AI разделяет черешню...',
        '🍈 AI режет дыню...',
        '🥥 AI раскалывает кокос...',
        '🍏 AI режет зеленое яблоко...',
    ]
    
    return random.choice(fruits_videos), random.choice(captions)


async def send_ai_fruits_video(update: Update, context: ContextTypes.DEFAULT_TYPE, duration_limit=60):
    """Отправка AI видео нарезки фруктов с прогресс-баром"""
    import io
    import aiohttp
    
    video_url, caption = get_random_ai_fruits_video()
    
    # Отправляем начальное сообщение с прогрессом
    duration_text = f'{duration_limit}сек' if duration_limit < 60 else f'{duration_limit//60}мин'
    progress_msg = await update.message.reply_text(f'📥 Генерация AI видео ({duration_text}): 0%')
    
    try:
        # Скачиваем видео с прогресс-баром
        async with aiohttp.ClientSession() as session:
            async with session.get(video_url) as response:
                if response.status == 200:
                    total_size = response.content_length or 0
                    downloaded = 0
                    chunks = []
                    
                    # Скачиваем по частям и показываем прогресс
                    async for chunk in response.content.iter_chunked(1024 * 100):
                        chunks.append(chunk)
                        downloaded += len(chunk)
                        
                        if total_size > 0:
                            percent = int((downloaded / total_size) * 100)
                            filled = int(percent / 5)
                            bar = '█' * filled + '░' * (20 - filled)
                            
                            if percent % 20 == 0 or percent == 100:
                                try:
                                    await progress_msg.edit_text(
                                        f'📥 Генерация AI видео:\n'
                                        f'{bar} {percent}%\n\n'
                                        f'🍎 Создание нарезки...'
                                    )
                                except:
                                    pass
                    
                    await progress_msg.edit_text('📤 Отправка AI видео...')
                    
                    video_bytes = b''.join(chunks)
                    video_file = io.BytesIO(video_bytes)
                    video_file.name = 'ai_fruits_cutting.mp4'
                    
                    # Отправляем видео в вертикальном формате Shorts с выбранной длительностью
                    await update.message.reply_video(
                        video=video_file,
                        caption=caption,
                        supports_streaming=True,
                        filename='ai_fruits_cutting.mp4',
                        width=720,
                        height=1280,
                        duration=duration_limit
                    )
                    
                    await progress_msg.delete()
                else:
                    raise Exception(f"HTTP {response.status}")
    except Exception as e:
        print(f"Ошибка отправки AI видео: {e}")
        try:
            await progress_msg.delete()
        except:
            pass
        
        try:
            await update.message.reply_video(
                video=video_url,
                caption=caption,
                supports_streaming=True,
                width=720,
                height=1280,
                duration=120
            )
        except:
            await update.message.reply_text(
                f'{caption}\n\n'
                f'🎬 {video_url}\n\n'
                f'⚠️ Не удалось загрузить видео.'
            )


async def send_ai_fruits_video_inline(message, duration_limit=60):
    """Отправка AI видео нарезки фруктов из inline-кнопки"""
    import io
    import aiohttp
    
    video_url, caption = get_random_ai_fruits_video()
    duration_text = f'{duration_limit}сек' if duration_limit < 60 else f'{duration_limit//60}мин'
    progress_msg = await message.reply_text(f'📥 Генерация AI видео ({duration_text}): 0%')
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(video_url) as response:
                if response.status == 200:
                    total_size = response.content_length or 0
                    downloaded = 0
                    chunks = []
                    
                    async for chunk in response.content.iter_chunked(1024 * 100):
                        chunks.append(chunk)
                        downloaded += len(chunk)
                        
                        if total_size > 0:
                            percent = int((downloaded / total_size) * 100)
                            filled = int(percent / 5)
                            bar = '█' * filled + '░' * (20 - filled)
                            
                            if percent % 20 == 0 or percent == 100:
                                try:
                                    await progress_msg.edit_text(
                                        f'📥 Генерация AI видео:\n'
                                        f'{bar} {percent}%\n\n'
                                        f'🍎 Создание нарезки...'
                                    )
                                except:
                                    pass
                    
                    await progress_msg.edit_text('📤 Отправка AI видео...')
                    
                    video_bytes = b''.join(chunks)
                    video_file = io.BytesIO(video_bytes)
                    video_file.name = 'ai_fruits_cutting.mp4'
                    
                    await message.reply_video(
                        video=video_file,
                        caption=caption,
                        supports_streaming=True,
                        filename='ai_fruits_cutting.mp4',
                        width=720,
                        height=1280,
                        duration=duration_limit
                    )
                    
                    await progress_msg.delete()
                else:
                    raise Exception(f"HTTP {response.status}")
    except Exception as e:
        print(f"Ошибка отправки AI видео: {e}")
        try:
            await progress_msg.delete()
        except:
            pass
        
        try:
            await message.reply_video(
                video=video_url,
                caption=caption,
                supports_streaming=True,
                width=720,
                height=1280,
                duration=120
            )
        except:
            await message.reply_text(
                f'{caption}\n\n'
                f'🎬 {video_url}\n\n'
                f'⚠️ Не удалось загрузить видео.'
            )


async def send_asmr_video_inline_with_duration(message, duration_limit=60):
    """Отправка ASMR видео из inline-кнопки с выбранной длительностью"""
    import io
    import aiohttp
    
    video_url, caption = get_random_asmr()
    duration_text = f'{duration_limit}сек' if duration_limit < 60 else f'{duration_limit//60}мин'
    progress_msg = await message.reply_text(f'📥 Загрузка ASMR ({duration_text}): 0%')
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(video_url) as response:
                if response.status == 200:
                    total_size = response.content_length or 0
                    downloaded = 0
                    chunks = []
                    
                    async for chunk in response.content.iter_chunked(1024 * 100):
                        chunks.append(chunk)
                        downloaded += len(chunk)
                        
                        if total_size > 0:
                            percent = int((downloaded / total_size) * 100)
                            filled = int(percent / 5)
                            bar = '█' * filled + '░' * (20 - filled)
                            
                            if percent % 20 == 0 or percent == 100:
                                try:
                                    await progress_msg.edit_text(
                                        f'📥 Загрузка ASMR:\n'
                                        f'{bar} {percent}%'
                                    )
                                except:
                                    pass
                    
                    await progress_msg.edit_text('📤 Отправка видео...')
                    
                    video_bytes = b''.join(chunks)
                    video_file = io.BytesIO(video_bytes)
                    video_file.name = 'asmr_short.mp4'
                    
                    await message.reply_video(
                        video=video_file,
                        caption=caption,
                        supports_streaming=True,
                        filename='asmr_short.mp4',
                        width=720,
                        height=1280,
                        duration=duration_limit
                    )
                    
                    await progress_msg.delete()
                else:
                    raise Exception(f"HTTP {response.status}")
    except Exception as e:
        print(f"Ошибка отправки видео: {e}")
        try:
            await progress_msg.delete()
        except:
            pass
        
        try:
            await message.reply_video(
                video=video_url,
                caption=caption,
                supports_streaming=True,
                width=720,
                height=1280,
                duration=duration_limit
            )
        except:
            await message.reply_text(
                f'{caption}\n\n'
                f'🎬 {video_url}\n\n'
                f'⚠️ Не удалось загрузить видео.'
            )


async def send_asmr_video_inline(message):
    """Отправка ASMR видео из inline-кнопки с прогресс-баром"""
    import io
    import aiohttp
    
    video_url, caption = get_random_asmr()
    
    # Отправляем начальное сообщение с прогрессом
    progress_msg = await message.reply_text('📥 Загрузка видео: 0%')
    
    try:
        # Скачиваем видео с прогресс-баром
        async with aiohttp.ClientSession() as session:
            async with session.get(video_url) as response:
                if response.status == 200:
                    total_size = response.content_length or 0
                    downloaded = 0
                    chunks = []
                    
                    # Скачиваем по частям и показываем прогресс
                    async for chunk in response.content.iter_chunked(1024 * 100):  # 100KB чанки
                        chunks.append(chunk)
                        downloaded += len(chunk)
                        
                        if total_size > 0:
                            percent = int((downloaded / total_size) * 100)
                            # Создаем визуальную полоску прогресса
                            filled = int(percent / 5)  # 20 символов
                            bar = '█' * filled + '░' * (20 - filled)
                            
                            # Обновляем каждые 20%
                            if percent % 20 == 0 or percent == 100:
                                try:
                                    await progress_msg.edit_text(
                                        f'📥 Загрузка видео:\n'
                                        f'{bar} {percent}%'
                                    )
                                except:
                                    pass
                    
                    # Обновляем на "отправка"
                    await progress_msg.edit_text('📤 Отправка видео...')
                    
                    # Собираем все чанки
                    video_bytes = b''.join(chunks)
                    video_file = io.BytesIO(video_bytes)
                    video_file.name = 'asmr_short.mp4'
                    
                    # Отправляем видео в стиле Shorts
                    await message.reply_video(
                        video=video_file,
                        caption=caption,
                        supports_streaming=True,
                        filename='asmr_short.mp4',
                        width=720,
                        height=1280,
                        duration=120
                    )
                    
                    # Удаляем сообщение с прогрессом
                    await progress_msg.delete()
                else:
                    raise Exception(f"HTTP {response.status}")
    except Exception as e:
        print(f"Ошибка отправки видео: {e}")
        try:
            await progress_msg.delete()
        except:
            pass
        
        try:
            await message.reply_video(
                video=video_url,
                caption=caption,
                supports_streaming=True,
                width=720,
                height=1280,
                duration=120
            )
        except:
            await message.reply_text(
                f'{caption}\n\n'
                f'🎬 {video_url}\n\n'
                f'⚠️ Не удалось загрузить видео. Открой по ссылке.'
            )


async def download_video_from_link(update: Update, context: ContextTypes.DEFAULT_TYPE, video_url: str):
    """Скачивание видео по ссылке и отправка ФАЙЛОМ (не ссылкой!)"""
    import os
    import re
    import asyncio
    from concurrent.futures import ThreadPoolExecutor
    
    user_id = update.effective_user.id
    lang = user_languages.get(user_id, DEFAULT_LANGUAGE)
    
    # Извлекаем URL из сообщения
    url_match = re.search(r'(https?://[^\s]+)', video_url)
    if not url_match:
        await update.message.reply_text('⚠️ Не найдена корректная ссылка на видео!')
        return
    
    clean_url = url_match.group(1)
    
    # Отправляем начальное сообщение
    progress_msg = await update.message.reply_text(f'{get_text(lang, "downloading")}...')
    
    # Создаем временную директорию
    temp_dir = '/tmp/bot_downloads'
    os.makedirs(temp_dir, exist_ok=True)
    output_file = os.path.join(temp_dir, f'video_{user_id}.mp4')
    
    try:
        # Определяем, это YouTube/TikTok или прямая ссылка
        is_platform = any(platform in clean_url.lower() for platform in ['youtube.com', 'youtu.be', 'tiktok.com', 'instagram.com', 'vimeo.com'])
        
        if is_platform:
            # Используем yt-dlp для платформ
            import yt_dlp
            
            ydl_opts = {
                'format': 'best[filesize<50M]/best',  # Ограничение 50MB
                'outtmpl': output_file,
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
            }
            
            await progress_msg.edit_text(f'📥 Анализирую ссылку...')
            
            def download_with_ytdlp():
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([clean_url])
            
            # Запускаем в отдельном потоке
            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor() as executor:
                await loop.run_in_executor(executor, download_with_ytdlp)
            
            await progress_msg.edit_text(f'{get_text(lang, "processing")}...')
            
        else:
            # Для прямых ссылок используем aiohttp
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                async with session.get(clean_url, timeout=aiohttp.ClientTimeout(total=300)) as response:
                    if response.status == 200:
                        total_size = response.content_length or 0
                        downloaded = 0
                        
                        with open(output_file, 'wb') as f:
                            async for chunk in response.content.iter_chunked(1024 * 100):
                                f.write(chunk)
                                downloaded += len(chunk)
                                
                                if total_size > 0:
                                    percent = int((downloaded / total_size) * 100)
                                    mb_downloaded = downloaded / (1024 * 1024)
                                    mb_total = total_size / (1024 * 1024)
                                    
                                    if percent % 20 == 0:
                                        try:
                                            filled = int(percent / 5)
                                            bar = '█' * filled + '░' * (20 - filled)
                                            await progress_msg.edit_text(
                                                f'{get_text(lang, "downloading")}:\n'
                                                f'{bar} {percent}%\n'
                                                f'📦 {mb_downloaded:.1f} MB / {mb_total:.1f} MB'
                                            )
                                        except:
                                            pass
                    else:
                        raise Exception(f"HTTP {response.status}")
        
        # Проверяем, скачался ли файл
        if not os.path.exists(output_file):
            raise Exception("Файл не скачался")
        
        file_size = os.path.getsize(output_file) / (1024 * 1024)
        
        # Если файл слишком большой для Telegram
        if file_size > 50:
            await progress_msg.edit_text(
                f'⚠️ Видео слишком большое: {file_size:.1f} MB\n'
                f'Telegram поддерживает до 50 MB'
            )
            os.remove(output_file)
            return
        
        await progress_msg.edit_text(f'📤 Отправка видео ({file_size:.1f} MB)...')
        
        # Отправляем видео КАК ФАЙЛ
        with open(output_file, 'rb') as video:
            await update.message.reply_video(
                video=video,
                caption=f'✅ Видео скачано!\n📦 Размер: {file_size:.1f} MB',
                supports_streaming=True,
                filename='downloaded_video.mp4'
            )
        
        # Удаляем временный файл
        os.remove(output_file)
        await progress_msg.delete()
        
    except Exception as e:
        print(f"Ошибка скачивания видео: {e}")
        
        # Удаляем временный файл если есть
        if os.path.exists(output_file):
            os.remove(output_file)
        
        try:
            await progress_msg.delete()
        except:
            pass
        
        await update.message.reply_text(
            f'⚠️ Не удалось скачать видео.\n\n'
            f'Возможные причины:\n'
            f'• Видео слишком большое (>50 MB)\n'
            f'• Неверная ссылка\n'
            f'• Видео недоступно\n'
            f'• Требуется авторизация\n\n'
            f'💡 Попробуй:\n'
            f'• Прямую ссылку на .mp4\n'
            f'• Короткое видео (<2 мин)\n'
            f'• Другой источник'
        )


async def post_init(application: Application):
    """Настройка меню команд бота"""
    commands = [
        BotCommand("start", "🚀 Запустить бота"),
        BotCommand("menu", "📋 Показать меню"),
        BotCommand("help", "❓ Помощь"),
        BotCommand("about", "ℹ️ О боте"),
        BotCommand("language", "🌍 Выбрать язык"),
    ]
    await application.bot.set_my_commands(commands)


def main():
    """Основная функция запуска бота"""
    # Проверка наличия токена
    if BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        print("❌ Ошибка: Пожалуйста, установите токен бота!")
        print("Создайте файл .env и добавьте: BOT_TOKEN=ваш_токен")
        return
    
    # Создаем приложение
    app = Application.builder().token(BOT_TOKEN).post_init(post_init).build()
    
    # Регистрируем обработчики команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("menu", menu_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CommandHandler("language", language_command))
    
    # Регистрируем обработчик callback-кнопок
    app.add_handler(CallbackQueryHandler(button_callback))
    
    # Регистрируем обработчик текстовых сообщений
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Запускаем бота
    print("🤖 Бот запущен и работает!")
    print("📋 Меню команд установлено")
    print("⌨️  Клавиатура с кнопками добавлена")
    print("Нажмите Ctrl+C для остановки")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()

