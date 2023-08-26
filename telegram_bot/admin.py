from django.contrib import admin
from .models import Flower, Florist, Courier, Consultation, Order

admin.site.register(Flower)
admin.site.register(Consultation)
admin.site.register(Order)


@admin.register(Courier)
class CourierAdmin(admin.ModelAdmin):
    list_display = ['id', 'telegram_id', 'name']


@admin.register(Florist)
class FloristAdmin(admin.ModelAdmin):
    list_display = ['id', 'telegram_id', 'name']
