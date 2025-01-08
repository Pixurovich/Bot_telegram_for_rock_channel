import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s', level=logging.INFO)

rock_genres = {}
rock_genre_images = {}
CHANNEL_USERNAME = ""

async def check_subscription(user_id, context):
    try:
        chat_member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return chat_member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        logging.error(f"Error checking subscription: {e}")
        return False

async def send_main_menu(update: Update, image_url: str = None):
    keyboard = [
        [InlineKeyboardButton("Алфавит", callback_data="alphabet")],
        [InlineKeyboardButton("Поджанры", callback_data="genres")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if image_url:
        await update.message.reply_photo(photo=image_url, caption='🎶 Привет, рок-энтузиаст! Готов отправиться в увлекательное музыкальное '
            'путешествие? Выбери способ поиска любимых клипов: По алфавиту – если ты знаешь, '
            'с какой буквы начинается твой любимый коллектив! По поджанрам – для тех, '
            'кто хочет исследовать разнообразие рок-музыки! Выбери вариант ниже:', reply_markup=reply_markup)
    else:
        await update.message.reply_text(
            '🎶 Привет, рок-энтузиаст! Готов отправиться в увлекательное музыкальное '
            'путешествие? Выбери способ поиска любимых клипов: По алфавиту – если ты знаешь, '
            'с какой буквы начинается твой любимый коллектив! По поджанрам – для тех, '
            'кто хочет исследовать разнообразие рок-музыки! Выбери вариант ниже:',
            reply_markup=reply_markup)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    image_url = 'https://logodix.com/logo/580915.png' 
    await send_main_menu(update, image_url=image_url)

async def send_search_options(update: Update):
    keyboard = [
        [InlineKeyboardButton("Алфавит", callback_data="alphabet")],
        [InlineKeyboardButton("Поджанры", callback_data="genres")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text(
        'Выбери способ поиска любимых клипов: По алфавиту или по поджанрам.',
        reply_markup=reply_markup)

async def check_subscription_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    is_subscribed = await check_subscription(user_id, context)

    query = update.callback_query
    await query.answer()

    if is_subscribed:
        # Кнопка для перехода к поиску
        keyboard = [[InlineKeyboardButton("Перейти к поиску", callback_data="go_to_search")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(text="Подписка проверена! Вы можете продолжать.", reply_markup=reply_markup)
    else:
        # Заменяем сообщение о вариантах поиска на сообщение о необходимости подписки
        keyboard = [
            [InlineKeyboardButton("Подписаться", url=f"t.me/{CHANNEL_USERNAME[1:]}")],
            [InlineKeyboardButton("Проверить подписку", callback_data="check_subscription")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text='Подписка не активна. Пожалуйста, подпишитесь на канал.',
            reply_markup=reply_markup
        )

async def go_to_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await send_search_options(update)
async def alphabet_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await verify_subscription_and_proceed(update, context, "alphabet")

async def genre_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await verify_subscription_and_proceed(update, context, "genres")

async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    image_url = 'https://logodix.com/logo/580915.png' 
    keyboard = [
        [InlineKeyboardButton("Алфавит", callback_data="alphabet")],
        [InlineKeyboardButton("Поджанры", callback_data="genres")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_photo(
        photo=image_url,
        caption='🎶 Привет, рок-энтузиаст! Готов отправиться в увлекательное музыкальное '
                'путешествие? \nВыбери способ поиска любимых клипов: По алфавиту – если ты знаешь, '
                'с какой буквы начинается твой любимый коллектив! По поджанрам – для тех, '
                'кто хочет исследовать разнообразие рок-музыки!',
        reply_markup=reply_markup
    )

    await query.message.delete()

async def send_alphabet_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Русский", callback_data="ru_alphabet")],
        [InlineKeyboardButton("Английский", callback_data="en_alphabet")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query = update.callback_query
    await query.answer()

    try:
        await query.edit_message_text(
            text='Выберите алфавит:',
            reply_markup=reply_markup
        )
    except Exception as e:
        logging.error(f"Ошибка при редактировании сообщения: {e}")
        await query.message.reply_text(
            text='Выберите алфавит:',
            reply_markup=reply_markup
        )

async def verify_subscription_and_proceed(update: Update, context: ContextTypes.DEFAULT_TYPE, callback_data: str):
    user_id = update.effective_user.id
    is_subscribed = await check_subscription(user_id, context)
    query = update.callback_query
    try:
        # Попытка ответить на callback_query
        await query.answer()

        if is_subscribed:
            if callback_data == "alphabet":
                await send_alphabet_selection(update, context)
            elif callback_data == "genres":
                await send_genre_selection(update, context)
        else:
            keyboard = [
                [InlineKeyboardButton("Подписаться", url=f"t.me/{CHANNEL_USERNAME[1:]}")],
                [InlineKeyboardButton("Проверить подписку", callback_data="check_subscription")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            try:
                # Используем edit_message_text для редактирования сообщения вместо повторного ответа на query
                await query.message.edit_text(
                    text='Пожалуйста, подпишитесь на канал и затем нажмите "Проверить подписку".',
                    reply_markup=reply_markup
                )
            except Exception as e:
                logging.error(f"Ошибка при редактировании сообщения: {e}")
                await query.message.reply_text(
                    text='Пожалуйста, подпишитесь на канал и затем нажмите "Проверить подписку".',
                    reply_markup=reply_markup
                )
    except Exception as e:
        logging.error(f"Ошибка при обработке callback_query: {e}")
        # В случае ошибки можно отправить сообщение обратно, например:
        await query.message.reply_text('Произошла ошибка при обработке запроса. Попробуйте снова.')

async def send_genre_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    genres = list(rock_genres.keys())
    keyboard = []
    buttons_per_row = 3 
    for i in range(0, len(genres), buttons_per_row):
        row = [InlineKeyboardButton(genre, callback_data=f"genre_{genre}") for genre in genres[i:i + buttons_per_row]]
        keyboard.append(row)

    keyboard.append([InlineKeyboardButton("Назад", callback_data="back")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    query = update.callback_query
    await query.answer()

    try:
        await query.edit_message_text(
            text='Выберите поджанр:',
            reply_markup=reply_markup
        )
    except Exception as e:
        logging.error(f"Ошибка при редактировании сообщения: {e}")
        await query.message.reply_text(
            text='Выберите поджанр:',
            reply_markup=reply_markup
        )

async def russian_alphabet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    letters = 'А В К М Н О П С Т'.split()
    keyboard = []

    for i in range(0, len(letters), 4):
        keyboard.append([InlineKeyboardButton(letter, callback_data=f"ru_{letter}") for letter in letters[i:i + 4]])
    keyboard.append([InlineKeyboardButton("Назад", callback_data="back")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text='Выбирай букву, на которую начинается твой любимый коллектив:', reply_markup=reply_markup)

async def english_alphabet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    letters = 'A B C D E F G H I K L M N O P Q R S T U V W'.split()
    keyboard = []

    for i in range(0, len(letters), 4):
        keyboard.append([InlineKeyboardButton(letter, callback_data=f"en_{letter}") for letter in letters[i:i + 4]])
    keyboard.append([InlineKeyboardButton("Назад", callback_data="back")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text='Выбирай букву, на которую начинается твой любимый коллектив:', reply_markup=reply_markup)
async def handle_alphabet_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "ru_alphabet":
        await russian_alphabet(update, context) 
    elif query.data == "en_alphabet":
        await english_alphabet(update, context)

async def handle_letter_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    letter = query.data.split('_')[1]
    # Фильтруем группы по первой букве
    bands = [band for genre in rock_genres.values() for band in genre.keys() if band.startswith(letter)]

    if bands:
        keyboard = []
        buttons_per_row = 2
        for i in range(0, len(bands), buttons_per_row):
            row = [InlineKeyboardButton(band, callback_data=band) for band in bands[i:i + buttons_per_row]]
            keyboard.append(row)
        keyboard.append([InlineKeyboardButton("Назад", callback_data="back")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=f'В этом списке – группы, начинающиеся на букву {letter}:\nВыбери свою '
                                           f'любимую команду и давай продолжим наше путешествие!',
                                       reply_markup=reply_markup)
    else:
        keyboard = [[InlineKeyboardButton("Назад", callback_data="back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=f'К сожалению, на выбранную букву {letter} пока не добавлено коллективов, но скоро они появятся.',
            reply_markup=reply_markup)

async def band_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    band = query.data
    genre = next(gen for gen in rock_genres if band in rock_genres[gen])
    tracks = rock_genres[genre][band]
    keyboard = []
    buttons_per_row = 3 
    track_items = list(tracks.items())
    for i in range(0, len(track_items), buttons_per_row):
        row = [InlineKeyboardButton(track, url=url) for track, url in track_items[i:i + buttons_per_row]]
        keyboard.append(row)

    keyboard.append([InlineKeyboardButton("Назад", callback_data="back")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    new_text = (f'🎵 Встречай творения группы {band}\nВот список их хитовых видеоклипов, которые '
                 f'точно заставят твое сердце биться в ритме рока. Выбирай трек и погружайся в '
                 f'мир невероятной музыки!')
    if query.message.text != new_text or query.message.reply_markup != reply_markup:
        try:
            await query.edit_message_text(text=new_text, reply_markup=reply_markup)
        except Exception as e:
            logging.error(f"Ошибка при редактировании сообщения: {e}")
            await query.message.reply_text(new_text, reply_markup=reply_markup)

async def handle_back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await back_to_menu(update, context)

async def select_genre(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    genre = query.data.split('_')[1]
    bands = list(rock_genres[genre].keys())

    buttons_per_row = 3
    keyboard = []

    for i in range(0, len(bands), buttons_per_row):
        row = [InlineKeyboardButton(band, callback_data=band) for band in bands[i:i + buttons_per_row]]
        keyboard.append(row)

    keyboard.append([InlineKeyboardButton("Назад к меню выбора вариантов поиска", callback_data="back")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text=f'🎸 Вот кто готов закрутить тебе голову звуками рока в поджанре {genre}:\n'
                                       f'Выбери свою любимую команду и давай продолжим наше путешествие!',
                                  reply_markup=reply_markup)

def main() -> None:
    app = ApplicationBuilder().token().build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_back, pattern='^back$'))
    app.add_handler(CallbackQueryHandler(back_to_menu, pattern='^back$'))
    app.add_handler(CallbackQueryHandler(alphabet_selection, pattern='^alphabet$'))
    app.add_handler(CallbackQueryHandler(genre_selection, pattern='^genres$'))
    app.add_handler(CallbackQueryHandler(check_subscription_handler, pattern='^check_subscription$'))
    app.add_handler(CallbackQueryHandler(select_genre, pattern='^genre_.*$'))
    app.add_handler(CallbackQueryHandler(handle_alphabet_choice, pattern='^(ru_alphabet|en_alphabet)$'))
    app.add_handler(CallbackQueryHandler(band_selection, pattern='|'.join(
        band for bands in rock_genres.values() for band in bands.keys())))
    app.add_handler(CallbackQueryHandler(go_to_search, pattern='^go_to_search$'))
    app.add_handler(CallbackQueryHandler(handle_letter_selection, pattern='^ru_[А-Я]$'))
    app.add_handler(CallbackQueryHandler(handle_letter_selection, pattern='^en_[A-Z]$'))

    app.run_polling()

if __name__ == '__main__':
    main()
