import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_shop.settings')
import django
from django.conf import settings

if not settings.configured:
    django.setup()

from telegram_bot.dispatcher import run_pooling


if __name__ == "__main__":
    run_pooling()