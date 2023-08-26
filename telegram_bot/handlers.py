from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import CallbackContext, ConversationHandler
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .models import Flower
import os


CHOOSE_OCCASION, CUSTOM_OCCASION_TEXT, CHOOSE_BUDGET, SHOW_FLOWER, ORDER_FLOWER, SEND_FLOWER = range(6)


def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("День рождения", callback_data='birthday')],
        [InlineKeyboardButton("Свадьба", callback_data='wedding')],
        [InlineKeyboardButton("Без повода", callback_data='no_reason')],
        [InlineKeyboardButton("Другой", callback_data='other')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Привет! К какому событию готовимся? Выберите один из вариантов, либо укажите свой:", reply_markup=reply_markup)
    return CHOOSE_OCCASION


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

    return SEND_FLOWER


def show_flower_and_buttons(update: Update, context: CallbackContext):
    print(f"context.user_data = {context.user_data}")
    if context.user_data.get("custom_occasion"):
        occasion = context.user_data["custom_occasion"]
    else:
        occasion = context.user_data["occasion"]
    approx_price = context.user_data["budget"]

    # flowers = get_filtered_flowers(occasion, approx_price)
    flowers = get_all_flowers()
    if not flowers:
        update.message.reply_text("Нет подходящих букетов")
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

    update.callback_query.message.reply_photo(photo=open(image_path, 'rb'))
    update.callback_query.message.reply_text(
        f"Название: {flower.name}\n"
        f"Описание: {flower.description}\n"
        f"Цена: {flower.price} руб."
    )

    keyboard = [
        [InlineKeyboardButton("Назад", callback_data='back'), InlineKeyboardButton("Вперёд", callback_data='forward')],
        [InlineKeyboardButton("Заказать", callback_data='order')],

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text(text="Посмотрите другие букеты или сделайте заказ", reply_markup=reply_markup)

    # keyboard2 = [
    #     [InlineKeyboardButton("Заказать консультацию", callback_data='onsulting')],
    #     [InlineKeyboardButton("Посмотреть всю коллекцию", callback_data='collection')],
    #
    # ]
    # reply_markup2 = InlineKeyboardMarkup(keyboard2)
    # update.callback_query.message.reply_text(text="Хотите что-то еще более уникальное? Подберите другой букет из нашей коллекции или закажите консультацию флориста",
    #                                          reply_markup=reply_markup2)


def button_click(update, context):
    query = update.callback_query
    query.answer()
    index = context.user_data["current_flower_index"]

    if query.data == "back":
        index = index - 1
    elif query.data == "forward":
        index = index + 1

    if index < 0:
        index = len(context.user_data["flowers"]) - 1
    elif index >= len(context.user_data["flowers"]):
        index = 0
    print(f"button_click: index = {index}")
    context.user_data["current_flower_index"] = index

    send_flower_info(update, context)


def get_filtered_flowers(occasion, approx_price):
    price_range = {
        "500": (500, 600),
        "1000": (1000, 1500),
        "2000": (2000, 3000),
        "more": 3000,
    }
    print(f"occasion, approx_price = {occasion} {approx_price}")
    if approx_price == "price_more":
        flowers_list = Flower.objects.filter(occasion=occasion, price__gte=price_range[approx_price])
    elif approx_price == "no_matter":
        flowers_list = Flower.objects.filter(occasion=occasion)
    else:
        flowers_list = Flower.objects.filter(occasion=occasion, price__range=price_range[approx_price])
    return flowers_list


def get_all_flowers():
    return Flower.objects.all()


def order_flower(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()


