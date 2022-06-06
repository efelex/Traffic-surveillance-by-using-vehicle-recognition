from django.db import models
import uuid
import uuid as uuid_lib
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from datetime import datetime

User = settings.AUTH_USER_MODEL
now = datetime.now().date()


# Create your models here.

class Car_registration(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False
    )
    owner_name = models.CharField(max_length=50)
    Owner_Id = models.IntegerField()
    car_model = models.CharField(max_length=200, null=False)
    owner_phone_number = PhoneNumberField()
    phone_number_assign = PhoneNumberField(blank=True, null=True)
    owner_email = models.EmailField()
    plate_number = models.CharField(max_length=20, unique=True)
    time_done = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.owner_name} ----- {self.plate_number}'

    class Meta:
        verbose_name_plural = 'Car Registration'
        ordering = ['-id']


class Insurance(models.Model):
    insurance_name = models.CharField(max_length=50)
    car = models.ForeignKey(Car_registration, on_delete=models.SET_NULL, null=True)
    insurance_duration_start = models.DateField()
    insurance_duration_end = models.DateField()
    time_done = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.insurance_name} --- {self.car.plate_number}'

    class Meta:
        verbose_name_plural = 'Insurance'


class Car_Control(models.Model):
    control_name = models.CharField(max_length=50)
    car = models.ForeignKey(Car_registration, on_delete=models.SET_NULL, null=True)
    control_start = models.DateField()
    control_end = models.DateField()
    time_done = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.control_name} --- {self.car.plate_number}'

    class Meta:
        verbose_name_plural = 'Car Control'


class Tax(models.Model):
    tax_name = models.CharField(max_length=50)
    car = models.ForeignKey(Car_registration, on_delete=models.SET_NULL, null=True)
    tax_start = models.DateField()
    tax_end = models.DateField()
    time_done = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.tax_name} --- {self.car.plate_number}'

    class Meta:
        verbose_name_plural = 'Tax'


class Captured(models.Model):
    police = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    car = models.ForeignKey(Car_registration, on_delete=models.SET_NULL, null=True)
    insurance_status = models.BooleanField()
    tax_status = models.BooleanField()
    control_status = models.BooleanField()
    time_done = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.police.name} --- {self.car.plate_number}'

    class Meta:
        verbose_name_plural = 'Captured'
        ordering = ['-time_done']


class Charged_car(models.Model):
    police = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    car = models.ForeignKey(Car_registration, on_delete=models.SET_NULL, null=True)
    insurance_charged = models.PositiveIntegerField(default=0)
    tax_charged = models.PositiveIntegerField(default=0)
    control_charged = models.PositiveIntegerField(default=0)
    insurance_ban_expire = models.DateField(blank=True, null=True)
    control_ban_expire = models.DateField(blank=True, null=True)
    tax_ban_expire = models.DateField(blank=True, null=True)
    time_done = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.car.plate_number} --- {self.time_done}'

    class Meta:
        verbose_name_plural = 'Charged Car'


class Charged_car_official(models.Model):
    police = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    car = models.ForeignKey(Car_registration, on_delete=models.SET_NULL, null=True, blank=True)
    insurance_charged_amount = models.PositiveIntegerField(default=0, null=True, blank=True)
    tax_charged_amount = models.PositiveIntegerField(default=0, null=True, blank=True)
    control_charged_amount = models.PositiveIntegerField(default=0, null=True, blank=True)
    insurance_tole_expire = models.DateField(null=True, blank=True)
    control_tole_expire = models.DateField(null=True, blank=True)
    tax_tole_expire = models.DateField(null=True, blank=True)

    time_done = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.car.plate_number} --- {self.time_done}'

    class Meta:
        verbose_name_plural = 'Charged Car Official'


class MoneyCharges(models.Model):
    insurance_charges = models.PositiveIntegerField()
    control_charges = models.PositiveIntegerField()
    tax_charges = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = 'Money charges'


class Dummy(models.Model):
    police = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    dummy_name = models.CharField(max_length=20, default='Dummy')
    time_done = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.police.name} --{self.dummy_name} ---- {self.time_done}'

    class Meta:
        verbose_name_plural = 'Dummy'


class Unregistered_car(models.Model):
    police = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    plate_number = models.CharField(max_length=50)
    time_done = models.DateTimeField(auto_now_add=True)
    danger = models.BooleanField()

    def __str__(self):
        return f'{self.police.name} --{self.plate_number} ---- {self.time_done}'

    class Meta:
        verbose_name_plural = 'Unregistered Car'


class Police_request(models.Model):
    status_check = [
        ('approved', 'approved'),
        ('pending', 'pending'),
        ('denied', 'denied')
    ]
    police = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    police_status = models.CharField(max_length=50, choices=status_check)
    time_done = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.police_status}'

    class Meta:
        verbose_name_plural = "Police Request"
        ordering = ['-id']
