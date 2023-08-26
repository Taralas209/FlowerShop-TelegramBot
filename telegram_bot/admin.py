from django.contrib import admin
from .models import Flower, Florist, Courier, Consultation, Order

admin.site.register(Flower)
admin.site.register(Florist)
admin.site.register(Courier)
admin.site.register(Consultation)
admin.site.register(Order)