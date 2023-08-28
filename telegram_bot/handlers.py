from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, InputMedia
from telegram.ext import CallbackContext, ConversationHandler
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .models import Flower
import os


CHOOSE_OCCASION, CUSTOM_OCCASION_TEXT, CHOOSE_BUDGET, SHOW_FLOWER, BUTTON_HANDLING, SEND_FLOWER, ORDER_FLOWER, CHOOSE_NAME, CHOOSE_SURNAME, CHOOSE_ADDRESS, CHOOSE_DATE, CHOOSE_TIME, CONSULTING = range(13)


def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("День рождения", callback_data='birthday')],
        [InlineKeyboardButton("Свадьба", callback_data='wedding')],
        [InlineKeyboardButton("В школу", callback_data='school')],
        [InlineKeyboardButton("Без повода", callback_data='no_reason')],
        [InlineKeyboardButton("Другой", callback_data='other')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Привет! К какому событию готовимся? Выберите один из вариантов, либо укажите свой:", reply_markup=reply_markup)
    return CHOOSE_OCCASION


def restart(update, context):
    user = update.message.from_user
    update.message.reply_text("Бот перезапущен!")
    context.user_data.clear()
    return start(update, context)


def choose_occasion(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    occasion = query.data

    if occasion == "other":
        query.message.reply_text("Введите повод:")
        return CUSTOM_OCCASION_TEXT
    else:
        context.user_data["occasion"] = occasion
        keyboard = [
            [InlineKeyboardButton("500", callback_data='500')],
            [InlineKeyboardButton("1000", callback_data='1000')],
            [InlineKeyboardButton("2000", callback_data='2000')],
            [InlineKeyboardButton("Больше", callback_data='more')],
            [InlineKeyboardButton("Не важно", callback_data='no_matter')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text("Выберите бюджет:", reply_markup=reply_markup)

    return CHOOSE_BUDGET


def show_budget_buttons(update: Update, _: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("500", callback_data='500')],
        [InlineKeyboardButton("1000", callback_data='1000')],
        [InlineKeyboardButton("2000", callback_data='2000')],
        [InlineKeyboardButton("Больше", callback_data='more')],
        [InlineKeyboardButton("Не важно", callback_data='no_matter')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Выберите бюджет:", reply_markup=reply_markup)


def custom_occasion_text(update: Update, context: CallbackContext):
    user_input = update.message.text
    context.user_data['custom_occasion'] = user_input

    update.message.reply_text(f"Какой другой повод: {user_input}")
    show_budget_buttons(update, context)
    return CHOOSE_BUDGET


def choose_budget(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    context.user_data["budget"] = query.data

    show_flower_and_buttons(update, context)

    return BUTTON_HANDLING


def show_flower_and_buttons(update: Update, context: CallbackContext):
    print(f"\ncontext.user_data = {context.user_data}\n")
    if context.user_data.get("custom_occasion"):
        occasion = None
    else:
        occasion = context.user_data["occasion"]
    approx_price = context.user_data["budget"]

    flowers = get_filtered_flowers(occasion, approx_price)
    if not flowers:
        update.callback_query.message.reply_text("Нет подходящих букетов")
        return ConversationHandler.END

    context.user_data["flowers"] = flowers
    context.user_data["current_flower_index"] = 0

    send_flower_info(update, context)


def send_flower_info(update, context):
    flowers = context.user_data["flowers"]
    index = context.user_data["current_flower_index"]

    flower = flowers[index]
    print(f"flower = {flower}")

    fs = FileSystemStorage()
    image_path = fs.url(flower.image.name)
    image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), image_path.lstrip('/'))

    flower_description = (
        f"Название: {flower.name}\n"
        f"Описание: {flower.description}\n"
        f"Цена: {flower.price} руб."
    )
    catalogue_message = update.callback_query.message.reply_photo(photo=open(image_path, 'rb'), caption=flower_description)
    keyboard = [
        [InlineKeyboardButton("Назад", callback_data='back'), InlineKeyboardButton("Вперёд", callback_data='forward')],
        [InlineKeyboardButton("Заказать", callback_data='order')],

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text(text="Посмотрите другие букеты или сделайте заказ", reply_markup=reply_markup)

    keyboard2 = [
        [InlineKeyboardButton("Заказать консультацию", callback_data='consulting')],
        [InlineKeyboardButton("Посмотреть всю коллекцию", callback_data='collection')],

    ]
    reply_markup2 = InlineKeyboardMarkup(keyboard2)
    update.callback_query.message.reply_text(text="Хотите что-то еще более уникальное? Подберите другой букет из нашей коллекции или закажите консультацию флориста",
                                             reply_markup=reply_markup2)

    context.user_data["catalogue_message_id"] = catalogue_message.message_id


def get_filtered_flowers(occasion, approx_price):
    price_range = {
        "500": (500, 600),
        "1000": (1000, 1500),
        "2000": (2000, 3000),
        "more": 3000,
    }
    print(f"\noccasion, approx_price = {occasion} {approx_price}\n")

    if occasion:
        flowers_list = Flower.objects.filter(occasion=occasion)
    else:
        flowers_list = Flower.objects.all()

    if approx_price == "more":
        flowers_list = flowers_list.filter(price__gte=price_range[approx_price])
    elif approx_price != "no_matter":
        flowers_list = flowers_list.filter(price__range=price_range[approx_price])

    return flowers_list


def get_all_flowers():
    return Flower.objects.all()


def button_handling(update: Update, context:  CallbackContext):
    query = update.callback_query
    query.answer()

    index = context.user_data["current_flower_index"]

    if query.data == "order":
        # There's a bouquet saved in user_data by now
        update.callback_query.message.reply_text("Начнем процесс заказа!")
        return ask_name(update, context)
    elif query.data == 'back':
        index = index - 1
        if index < 0:
            index = len(context.user_data["flowers"]) - 1
        context.user_data["current_flower_index"] = index
        return update_catalogue(update, context)
    elif query.data == 'forward':
        index = index + 1
        if index >= len(context.user_data["flowers"]):
            index = 0
        context.user_data["current_flower_index"] = index
        return update_catalogue(update, context)
    elif query.data == 'consulting':
        update.callback_query.message.reply_text("Укажите номер телефона, и наш флорист перезвонит вам в течение 20 минут")
        return get_number_for_consulting(update, context)
    elif query.data == 'collection':
        print("Пользователь нажал кнопку Коллекция")
        update.callback_query.message.reply_text("Вот вся наша коллеция:")
        context.user_data["flowers"] = get_all_flowers()
        send_flower_info(update, context)


def update_catalogue(update, context):
    query = update.callback_query
    query.answer()
    catalogue_message_id = context.user_data["catalogue_message_id"]

    flowers = context.user_data["flowers"]
    index = context.user_data["current_flower_index"]

    flower = flowers[index]
    fs = FileSystemStorage()
    image_path = fs.url(flower.image.name)
    image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), image_path.lstrip('/'))

    flower_description = (
        f"Название: {flower.name}\n"
        f"Описание: {flower.description}\n"
        f"Цена: {flower.price} руб."
    )

    with open(image_path, "rb") as new_image:
        new_photo = InputMediaPhoto(
            media=new_image,
            caption=flower_description
        )

        context.bot.edit_message_media(
            message_id=catalogue_message_id,
            chat_id=query.message.chat_id,
            media=new_photo,
        )


def ask_name(update: Update, context: CallbackContext):
    update.callback_query.message.reply_text("Пожалуйста, введите ваше имя:")
    return CHOOSE_SURNAME


def ask_surname(update: Update, context: CallbackContext):
    context.user_data["name"] = update.message.text
    update.message.reply_text("Теперь введите вашу фамилию:")
    return CHOOSE_ADDRESS


def ask_address(update: Update, context: CallbackContext):
    context.user_data["surname"] = update.message.text
    update.message.reply_text("Введите ваш адрес:")
    return CHOOSE_DATE


def ask_date(update: Update, context: CallbackContext):
    context.user_data["adress"] = update.message.text
    update.message.reply_text("Введите дату доставки:")
    return CHOOSE_TIME


def ask_time(update: Update, context: CallbackContext):
    context.user_data["date"] = update.message.text
    update.message.reply_text("Введите время доставки:")
    return ORDER_FLOWER


def get_order(update: Update, context: CallbackContext):
    context.user_data["time"] = update.message.text
    print(context.user_data)


def get_number_for_consulting(update: Update, context: CallbackContext):
    update.callback_query.message.reply_text("Пожалуйста, введите ваш номер телефона:")
    return CONSULTING
