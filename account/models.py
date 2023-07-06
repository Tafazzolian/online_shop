from django.db import models
from django.contrib.auth.models import AbstractBaseUser,AbstractUser
from .managers import UserManager
from datetime import timedelta, datetime


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    full_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email','full_name'] #required fields when making a user in shell by createsuper user

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_lable):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now= True)
    created2 = datetime.now()


    def __str__(self):
        return f'{self.phone_number} - {self.code} - {self.created}'