from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from telegram_bot.models import Flower


CUSTOM_OCCASION, PRICES, OCCASION_HANDLER = range(3)
END = -1
# def order_flower(update: Update, context: CallbackContext):
#     query = update.callback_query
#     query.answer()
#     show_flower(update, context)
#
#
# def show_flower(update: Update, context: CallbackContext):
#
#     flower = Flower.objects.first()
#     query = update.callback_query
#
#     if flower is not None:
#         text = f"{flower.name}\n{flower.description}\nЦена: {flower.price} руб.\nПодходит для: {flower.get_occasion_display()}"
#         query.message.reply_text(text)
#     else:
#         query.message.reply_text("К сожалению, цветы в наличии отсутствуют.")


def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Заказать", callback_data='order')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Привет! Хотите заказать цветы?")
    update.message.reply_text("Нажмите кнопку ниже, чтобы сделать заказ:", reply_markup=reply_markup)


def show_occasions(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("День рождения", callback_data="birthday"),
            InlineKeyboardButton("Без повода", callback_data="no_reason")
        ],
        [
            InlineKeyboardButton("Другой повод", callback_data="other_occasion")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    print(query)
    query.message.reply_text("Выберите повод:", reply_markup=reply_markup)

    return OCCASION_HANDLER


def occasion_handler(update, context):
    query = update.callback_query
    query.answer()
    print(query)
    user_choice = query.data
    print(user_choice)
    if user_choice == "other_occasion":
        return CUSTOM_OCCASION
    else:
        return PRICES


def show_prices(update, context):
    query = update.callback_query
    query.answer()
    print(query)
    if update.message:
        context.chat_data["occasion"] = update.message.text
    else:
        context.chat_data["occasion"] = query.data
    print(context.chat_data)
    keyboard = [
        [InlineKeyboardButton("~500", callback_data="price_500")],
        [InlineKeyboardButton("~1000", callback_data="price_1000")],
        [InlineKeyboardButton("~2000", callback_data="price_2000")],
        [InlineKeyboardButton("Больше", callback_data="price_more")],
        [InlineKeyboardButton("Не важно", callback_data="price_none")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text("На какую сумму рассчитываете?", reply_markup=reply_markup)

    return END


def ask_for_occasion(update, context):
    query = update.callback_query
    query.answer()
    query.message.reply_text("Опишите ваш повод")

    return PRICES


def get_filtered_flowers(occasion, approx_price):
    price_range = {
        "price_500": (500, 600),
        "price_1000": (1000, 1500),
        "price_2000": (2000, 3000),
        "price_more": 3000,
    }
    if approx_price == "price_more":
        flowers_list = Flower.objects.filter(occasion=occasion, price__gte=price_range[approx_price])
    elif approx_price == "price_none":
        flowers_list = Flower.objects.filter(occasion=occasion)
    else:
        flowers_list = Flower.objects.filter(occasion=occasion, price__range=price_range[approx_price])
    return flowers_list
