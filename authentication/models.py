from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from django.utils import timezone

now = timezone.now()
# User = settings.AUTH_USER_MODEL


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, phone_number, name, password=None, **extra_fields):
        """
        Creates and saves a User with the given phone and password.
        """
        if not phone_number:
            raise ValueError('Users must have an phone address')
        if not name:
            raise ValueError('Users must have name')

        user = self.model(
            phone_number=phone_number,
            name=name,

        )
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_staffuser(self, phone_number, name, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        if not phone_number:
            raise ValueError('Users must have an phone address')
        if not name:
            raise ValueError('Users must have name')
        user = self.create_user(

            phone_number,
            name=name,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, name, password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            phone_number,
            name,
            password=password,
        )

        user.staff = True
        user.admin = True
        user.is_verified = True

        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    name = models.CharField(max_length=255, null=False)
    phone_number = PhoneNumberField(unique=True)
    is_verified = models.BooleanField(default=False)
    is_verified_police = models.BooleanField(default=False)
    # username = None

    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name']
    objects = UserManager()

    def get_full_name(self):
        return self.phone_number

    def get_short_name(self):
        return self.phone_number

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_image = models.ImageField(upload_to='images/', default='profile.png', )
    date_of_birth = models.DateField(max_length=250, blank=True, null=True)
    id_number = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.name} -- {self.user.phone_number}'
