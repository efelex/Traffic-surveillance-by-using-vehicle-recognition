from django.db import models
from car_plate.models import Car_registration


# Create your models here.

class Payment_completed(models.Model):
    car = models.ForeignKey(Car_registration, on_delete=models.CASCADE)
    insurance_payment = models.PositiveIntegerField(null=True, blank=True)
    tax_payment = models.PositiveIntegerField(null=True, blank=True)
    control_payment = models.PositiveIntegerField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Payment completed'
        ordering = ['date', ]

    def __str__(self):
        return f'{self.car.owner_phone_number}  --- {self.car.plate_number}'
