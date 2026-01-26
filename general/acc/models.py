from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    
    class Status(models.TextChoices):
        VLAD = 'VLAD', 'Vlad'
        SUPERVLAD = 'SUPERVLAD', 'Super-Vlad'
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.VLAD)

    def __str__(self):
        return self.user.username