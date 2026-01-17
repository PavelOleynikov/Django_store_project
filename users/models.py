from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(verbose_name="почта", unique=True)
    phone_number = models.CharField(verbose_name="номер телефона", max_length=15, blank=True, null=True)
    avatar = models.ImageField(verbose_name="аватар", upload_to="avatars/", blank=True, null=True)
    country = models.CharField(verbose_name="страна", max_length=50, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
