import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext, Updater, CallbackQueryHandler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_shop.settings')
import django
django.setup()


def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Заказать", callback_data='order')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Привет! Хотите заказать цветы?")
    update.message.reply_text("Нажмите кнопку ниже, чтобы сделать заказ:", reply_markup=reply_markup)


def order_flower(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    show_flower(update, context)


def show_flower(update: Update, context: CallbackContext):
    from telegram_bot.models import Flower
    flower = Flower.objects.first()
    query = update.callback_query

    if flower is not None:
        text = f"{flower.name}\n{flower.description}\nЦена: {flower.price} руб.\nПодходит для: {flower.get_occasion_display()}"
        query.message.reply_text(text)
    else:
        query.message.reply_text("К сожалению, цветы в наличии отсутствуют.")



def main():
    load_dotenv()
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    updater = Updater(TELEGRAM_TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(order_flower, pattern='order'))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()