import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_shop.settings')
django.setup()

from telegram import Bot
from .models import Flower, Florist, Courier, Consultation, Order
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = Bot(TELEGRAM_TOKEN)


def send_order_to_courier(update, context, order):
    order_text = f"""
        Название букета: {order.flower.name}
        Цена букета: {order.flower.price}
        Имя: {order.first_name}
        Фамилия: {order.last_name}
        Адрес: {order.address}
        Дата и время доставки: {order.delivery_date} {order.delivery_time}
        """
    try:
        courier = Courier.objects.first()
        if courier:
            bot.send_message(
                chat_id=courier.telegram_id,
                text=order_text
            )
    except Exception as e:
        print(f"Error sending order to courier: {e}")


def send_number_to_florist(update, context, consultation):
    try:
        florist = Florist.objects.first()
        if florist:
            bot.send_message(
                chat_id=florist.telegram_id,
                text=f"Новая консультация:\nПричина: {consultation.reason}\nБюджет: {consultation.budget}\nНомер: {consultation.number}"
            )
    except Exception as e:
        print(f"Error sending message to florist: {e}")
