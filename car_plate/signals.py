from django.db.models.signals import post_save
from django.dispatch import receiver
from car_plate.models import Charged_car, Charged_car_official, Police_request
import datetime
from authentication.models import User
import asyncio
import time

today_year_exact = datetime.date.today()


@receiver(post_save, sender=Charged_car)
def create_official_charged(sender, instance, created, **kwargs):
    if created:
        police_info = instance.police
        car_info = instance.car
        tax_charged = instance.tax_charged
        insurance_amount = instance.insurance_charged
        control_charged = instance.control_charged

        Charged_car_official.objects.create(police=police_info, car=car_info, insurance_charged_amount=insurance_amount,
                                            tax_charged_amount=tax_charged, control_charged_amount=control_charged)


@receiver(post_save, sender=Charged_car)
def update_official_ban(sender, instance, created, **kwargs):
    if not created:
        car_info = instance.car
        charged_check = Charged_car_official.objects.filter(car=car_info).first()
        if charged_check:
            insurance_amount = instance.insurance_charged
            control_charged = instance.control_charged
            tax_charged = instance.tax_charged

            if charged_check.insurance_charged_amount < insurance_amount:
                insurance_amount = instance.insurance_charged
            else:
                insurance_amount = charged_check.insurance_charged_amount
            if charged_check.control_charged_amount < control_charged:
                control_amount = instance.control_charged
            else:
                control_amount = charged_check.control_charged_amount
            if charged_check.tax_charged_amount < tax_charged:
                tax_amount = instance.tax_charged
            else:
                tax_amount = charged_check.tax_charged_amount

            Charged_car_official.objects.filter(car=car_info).update(insurance_charged_amount=insurance_amount,
                                                                     tax_charged_amount=tax_amount,
                                                                     control_charged_amount=control_amount)
            print("time-done")


@receiver(post_save, sender=Police_request)
def change_police_status(sender, instance, created, **kwargs):
    if not created:
        new_status = instance.police_status
        phone_number = instance.police.phone_number
        if new_status == 'approved':
            User.objects.filter(phone_number=phone_number).update(is_verified_police=True)
