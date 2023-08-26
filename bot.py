import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_shop.settings')
import django
django.setup()

from dotenv import load_dotenv
from telegram_bot.handlers import start, choose_occasion, choose_budget, custom_occasion_text, button_handling, ask_name, ask_surname, ask_address, ask_date, ask_time, get_order, get_number_to_florist, create_order, show_collections, restart
from telegram_bot.handlers import CHOOSE_OCCASION, CHOOSE_BUDGET, CUSTOM_OCCASION_TEXT, BUTTON_HANDLING, CHOOSE_NAME, CHOOSE_SURNAME, CHOOSE_ADDRESS, CHOOSE_DATE, CHOOSE_TIME, ORDER_FLOWER, GETTING_NUMBER, CREATE_ORDER, SHOW_COLLECTIONS
from telegram.ext import CommandHandler, CallbackContext, Updater, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters

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
            BUTTON_HANDLING: [CallbackQueryHandler(button_handling)],
            CHOOSE_NAME: [MessageHandler(Filters.text & ~Filters.command, ask_name)],
            CHOOSE_SURNAME: [MessageHandler(Filters.text & ~Filters.command, ask_surname)],
            CHOOSE_ADDRESS: [MessageHandler(Filters.text & ~Filters.command, ask_address)],
            CHOOSE_DATE: [MessageHandler(Filters.text & ~Filters.command, ask_date)],
            CHOOSE_TIME: [MessageHandler(Filters.text & ~Filters.command, ask_time)],
            ORDER_FLOWER: [MessageHandler(Filters.text & ~Filters.command, get_order)],
            GETTING_NUMBER: [MessageHandler(Filters.text & ~Filters.command, get_number_to_florist)],
            CREATE_ORDER: [CallbackQueryHandler(create_order, pattern='^confirm_order$')],
            SHOW_COLLECTIONS: [CallbackQueryHandler(show_collections)],
        },
        fallbacks=[CommandHandler('restart', restart)],
    )

    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler('restart', restart))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()