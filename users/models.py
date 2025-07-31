from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    company_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Название организации")

    # Убираем стандартные поля имени и фамилии
    first_name = None
    last_name = None

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.company_name or self.username
