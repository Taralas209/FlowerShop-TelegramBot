import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_shop.settings')
import django
django.setup()

from dotenv import load_dotenv
from telegram_bot import handlers
from telegram.ext import CommandHandler, CallbackContext, Updater, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters


def main():
    load_dotenv()
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    updater = Updater(telegram_token)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', handlers.start)],
        states={
            handlers.CHOOSE_OCCASION: [CallbackQueryHandler(handlers.choose_occasion)],
            handlers.CUSTOM_OCCASION_TEXT: [
                MessageHandler(Filters.text & ~Filters.command, handlers.custom_occasion_text)
            ],
            handlers.CHOOSE_BUDGET: [CallbackQueryHandler(handlers.choose_budget)],
            handlers.SHOW_FLOWER: [CallbackQueryHandler(handlers.show_flower_and_buttons)],
            handlers.SEND_FLOWER: [CallbackQueryHandler(handlers.button_click)]
        },
        fallbacks=[],
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
