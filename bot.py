import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_shop.settings')
import django
django.setup()

from dotenv import load_dotenv
from telegram_bot.handlers import start, choose_occasion, choose_budget, custom_occasion_text, show_flower_and_buttons, order_flower, input_name,show_consult_buttons, input_name,input_address,input_date_time
from telegram_bot.handlers import CHOOSE_OCCASION, CHOOSE_BUDGET, CUSTOM_OCCASION_TEXT, SHOW_FLOWER_AND_BUTTONS, ORDER_FLOWER, INPUT_NAME, SHOW_CONSULT_BUTTONS,INPUT_ADDRESS,INPUT_DATE_TIME
from telegram.ext import CommandHandler, CallbackContext, Updater, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters

def main():
    load_dotenv()
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    updater = Updater(TELEGRAM_TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(order_flower, pattern='order'))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSE_OCCASION: [CallbackQueryHandler(choose_occasion)],
            CUSTOM_OCCASION_TEXT: [MessageHandler(Filters.text & ~Filters.command, custom_occasion_text)],
            CHOOSE_BUDGET: [CallbackQueryHandler(choose_budget)],
            SHOW_FLOWER_AND_BUTTONS: [CallbackQueryHandler(show_flower_and_buttons)],
            SHOW_CONSULT_BUTTONS: [CallbackQueryHandler(show_consult_buttons)],
            ORDER_FLOWER:[CallbackQueryHandler(order_flower)],
            INPUT_NAME:[MessageHandler(Filters.text & ~Filters.command, input_name)],
            INPUT_ADDRESS:[MessageHandler(Filters.text & ~Filters.command, input_address)],
            INPUT_DATE_TIME:[MessageHandler(Filters.text & ~Filters.command, input_date_time)],
        },
        fallbacks=[],
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()