from django.db import models

class Flower(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='flowers/')
    OCCASIONS_CHOICES = [
        ('birthday', 'День рождения'),
        ('wedding', 'Свадьба'),
        ('school', 'В школу'),
        ('no_reason', 'Без повода'),
        ('other', 'Другой повод'),
    ]
    occasion = models.CharField(max_length=20, choices=OCCASIONS_CHOICES, default='no_reason')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Букет"
        verbose_name_plural = "Букеты"

class Florist(models.Model):
    telegram_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name or str(self.telegram_id)

    class Meta:
        verbose_name = "Флорист"
        verbose_name_plural = "Флористы"


class Courier(models.Model):
    telegram_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name or str(self.telegram_id)

    class Meta:
        verbose_name = "Курьер"
        verbose_name_plural = "Курьеры"


class Consultation(models.Model):
    reason = models.CharField(max_length=200)
    budget = models.PositiveIntegerField()
    number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reason} - {self.budget} - {self.number}"

    class Meta:
        verbose_name = "Консультация"
        verbose_name_plural = "Консультации"


class Order(models.Model):
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE, verbose_name='Букет')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    address = models.TextField(verbose_name='Адрес')
    delivery_date = models.DateField(verbose_name='Дата доставки')
    delivery_time = models.TimeField(verbose_name='Время доставки')
    order_created_date = models.DateTimeField(auto_now_add=True)
    order_created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заказ №{self.id} на {self.delivery_date} {self.delivery_time}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"