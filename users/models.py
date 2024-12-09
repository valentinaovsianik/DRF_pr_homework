from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Email")  # Авторизация по email
    phone = models.CharField(max_length=15, verbose_name="Телефон", blank=True, null=True)
    city = models.CharField(max_length=100, verbose_name="Город", blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", verbose_name="Аватарка", blank=True, null=True)

    # Заменяем username на email для авторизации
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email