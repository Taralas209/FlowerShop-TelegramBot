from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import CallbackContext
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .models import Flower
import os


CHOOSE_OCCASION, CUSTOM_OCCASION_TEXT, CHOOSE_BUDGET, BUTTON_HANDLING, ORDER_FLOWER, CHOOSE_NAME, CHOOSE_SURNAME, CHOOSE_ADDRESS, CHOOSE_DATE, CHOOSE_TIME, CONSULTING, END = range(12)


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
    reason = query.data

    if reason == "other":
        query.message.reply_text("Введите повод:")
        return CUSTOM_OCCASION_TEXT
    else:
        context.user_data["reason"] = reason
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
    flower = Flower.objects.order_by('?').first()

    fs = FileSystemStorage()
    image_path = fs.url(flower.image.name)
    image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), image_path.lstrip('/'))

    update.callback_query.message.reply_photo(photo=open(image_path, 'rb'))
    update.callback_query.message.reply_text(f"Название: {flower.name}\n"
                              f"Описание: {flower.description}\n"
                              f"Цена: {flower.price} руб.")

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


def button_handling(update: Update, context:  CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == "order":
        update.callback_query.message.reply_text("Начнем процесс заказа!")
        return ask_name(update, context)
    elif query.data == 'back':
        print("Пользователь нажал кнопку 'Назад'")
    elif query.data == 'forward':
        print("Пользователь нажал кнопку 'Вперёд'")
    elif query.data == 'consulting':
        update.callback_query.message.reply_text("Укажите номер телефона, и наш флорист перезвонит вам в течение 20 минут")
        return get_number_for_consulting(update, context)
    elif query.data == 'collection':
        print("Пользователь нажал кнопку Коллекция")


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