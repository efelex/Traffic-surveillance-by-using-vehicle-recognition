from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings

User = settings.AUTH_USER_MODEL


# Create your models here.

class Send_message(models.Model):
    police_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    receiver_message = PhoneNumberField()
    subject_message = models.CharField(max_length=100)
    body_message = models.TextField(max_length=250)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.police_user.phone_number} ---- {self.police_user.name}'

    class Meta:
        verbose_name_plural = "Send message"
        ordering = ['-date']
