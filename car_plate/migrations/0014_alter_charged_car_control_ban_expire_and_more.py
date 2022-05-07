# Generated by Django 4.0.2 on 2022-05-07 22:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_plate', '0013_alter_charged_car_control_ban_expire_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charged_car',
            name='control_ban_expire',
            field=models.DateField(blank=True, default=datetime.date(2022, 5, 8), null=True),
        ),
        migrations.AlterField(
            model_name='charged_car',
            name='insurance_ban_expire',
            field=models.DateField(blank=True, default=datetime.date(2022, 5, 8), null=True),
        ),
        migrations.AlterField(
            model_name='charged_car',
            name='tax_ban_expire',
            field=models.DateField(blank=True, default=datetime.date(2022, 5, 8), null=True),
        ),
    ]
