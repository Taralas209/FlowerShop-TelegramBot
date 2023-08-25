import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import CommandHandler, ConversationHandler, Updater, CallbackQueryHandler, Filters


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_shop.settings')
import django
django.setup()
import handlers


conversation_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(handlers.show_occasions, pattern='order')
    ],
    states={
        handlers.CUSTOM_OCCASION: [CallbackQueryHandler(handlers.ask_for_occasion)],
        handlers.PRICES: [CallbackQueryHandler(handlers.show_prices)],
        handlers.OCCASION_HANDLER: [CallbackQueryHandler(handlers.occasion_handler)]
    },
    fallbacks=[]
)


def main():
    load_dotenv()
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    updater = Updater(telegram_token)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", handlers.start))
    dp.add_handler(conversation_handler)
    # dp.add_handler(CallbackQueryHandler(handlers.show_occasions, pattern='order'))
    # dp.add_handler(CallbackQueryHandler(handlers.show_prices, pattern="^birthday|no_reason|user_occasion$"))
    # dp.add_handler(CallbackQueryHandler(handlers.ask_for_occasion, pattern="occasion_other"))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

