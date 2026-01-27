from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    class Status(models.TextChoices):
        VLAD = 'VLAD', 'Vlad'
        SUPERVLAD = 'SUPERVLAD', 'Super-Vlad'
    SUPER = Status.SUPERVLAD
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.VLAD)

    def __str__(self):
        return self.username