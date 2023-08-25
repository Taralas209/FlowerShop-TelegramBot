import os
from dotenv import load_dotenv
from telegram_bot.handlers import start, choose_occasion, choose_budget, custom_occasion_text
from telegram_bot.handlers import CHOOSE_OCCASION, CHOOSE_BUDGET, CUSTOM_OCCASION_TEXT

from telegram.ext import CommandHandler, CallbackContext, Updater, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_shop.settings')
import django
django.setup()


def main():
    load_dotenv()
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    updater = Updater(TELEGRAM_TOKEN)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSE_OCCASION: [CallbackQueryHandler(choose_occasion)],
            CUSTOM_OCCASION_TEXT: [MessageHandler(Filters.text & ~Filters.command, custom_occasion_text)],
            CHOOSE_BUDGET: [CallbackQueryHandler(choose_budget)],
        },
        fallbacks=[],
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()