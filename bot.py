import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_shop.settings')
import django
django.setup()

from dotenv import load_dotenv
from telegram_bot.handlers import start, choose_occasion, choose_budget, custom_occasion_text, show_flower_and_buttons
from telegram_bot.handlers import CHOOSE_OCCASION, CHOOSE_BUDGET, CUSTOM_OCCASION_TEXT, SHOW_FLOWER
from telegram.ext import CommandHandler, CallbackContext, Updater, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters


def main():
    load_dotenv()
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    updater = Updater(telegram_token)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSE_OCCASION: [CallbackQueryHandler(choose_occasion)],
            CUSTOM_OCCASION_TEXT: [MessageHandler(Filters.text & ~Filters.command, custom_occasion_text)],
            CHOOSE_BUDGET: [CallbackQueryHandler(choose_budget)],
            # SHOW_FLOWER: [CallbackQueryHandler(show_flower)],
        },
        fallbacks=[],
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
