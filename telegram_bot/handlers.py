from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext


CHOOSE_OCCASION, CUSTOM_OCCASION_TEXT, CHOOSE_BUDGET, SHOW_FLOWER, ORDER_FLOWER, END = range(6)


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
    print(context.user_data)

    return SHOW_FLOWER


