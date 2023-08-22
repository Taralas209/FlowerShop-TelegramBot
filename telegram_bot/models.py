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
