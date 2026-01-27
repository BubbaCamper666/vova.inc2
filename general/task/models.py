from django.db import models
import uuid
from acc.models import User
from django.conf import settings
from django.core.exceptions import ValidationError

class Team(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        ACTIVE = 'ACTIVE', 'Active'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)

    title = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    createDate = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date created"
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="teams",
        limit_choices_to={'status': User.SUPER}
    )

    def clean(self):
        if self.owner and self.owner.status != User.SUPER:
            raise ValidationError({
                'owner': 'Владельцем проекта может быть только Super-Vlad'
            })
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class TeamMember(models.Model):
    class Role(models.TextChoices):
        GUFICK = 'GUFICK', 'Gufick'
        VLAD = 'VLAD', 'Vlad'
        VOVA = 'VOVA', 'Vova'
        MAX = 'MAX', 'Max'

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="teams"
    )

    role = models.CharField(max_length=30, choices=Role.choices, default=Role.GUFICK)

class Task(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        ACTIVE = 'ACTIVE', 'Active'

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)

    title = models.CharField(max_length=30)
    description = models.CharField(max_length=300)

    createDate = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date created"
    )

    deadline = models.DateTimeField(
        verbose_name="deadline",
        null = True,
        blank=True
    )

class TaskMember(models.Model):
    class Role(models.TextChoices):
        GUFICK = 'GUFICK', 'Gufick'
        VLAD = 'VLAD', 'Vlad'
        VOVA = 'VOVA', 'Vova'
        MAX = 'MAX', 'Max'

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="teams"
    )

    role = models.CharField(max_length=30, choices=Role.choices, default=Role.GUFICK)
