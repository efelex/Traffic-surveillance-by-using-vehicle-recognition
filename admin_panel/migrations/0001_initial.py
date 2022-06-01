# Generated by Django 4.0.2 on 2022-06-01 15:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Send_message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receiver_message', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('subject_message', models.CharField(max_length=100)),
                ('body_message', models.TextField(max_length=250)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('police_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Send message',
                'ordering': ['-date'],
            },
        ),
    ]
