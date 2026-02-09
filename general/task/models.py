from django.db import models
import uuid
from acc.models import User
from django.conf import settings
from django.core.exceptions import ValidationError
from django.urls import reverse

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
        related_name="owner",
        limit_choices_to={'status': User.SUPER},
        null=True,
        blank=True
    )

    def clean(self):
        if self.owner and self.owner.status != User.SUPER:
            raise ValidationError({
                'owner': 'Владельцем проекта может быть только Super-Vlad'
            })
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("teamdetail", kwargs={"pk": self.id})
    
    def get_members_url(self):
        return reverse("teammembers", kwargs={"pk": self.id})
    
    def get_tasks_url(self):
        return reverse("tasklist", kwargs={"pk": self.id})

class TeamMember(models.Model):
    class Role(models.TextChoices):
        GUFICK = 'GUFICK', 'Gufick'
        VLAD = 'VLAD', 'Vlad'
        VOVA = 'VOVA', 'Vova'
        MAX = 'MAX', 'Max'

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="users_team"
    )

    profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="users_profile"
    )

    role = models.CharField(max_length=30, choices=Role.choices, default=Role.GUFICK)

    def __str__(self):
        return self.title
    
    def get_deletion_url(self):
        return reverse("delete_team_member", kwargs={"pk": self.team.id, "member_id": self.id})


class Task(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        ACTIVE = 'ACTIVE', 'Active'

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="parent_team"
    )

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)

    id = models.BigAutoField(primary_key=True)

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
   

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("taskdetail", kwargs={"pk": self.id})
    
    def get_members_url(self):
        return reverse("taskmembers", kwargs={"pk": self.team.id, "taskid": self.id})
    
    def get_delete_url(self):
        return reverse("taskdelete", kwargs={"pk": self.team.id, "taskid": self.id})
    

    
class TaskMember(models.Model):
    class Role(models.TextChoices):
        GUFICK = 'GUFICK', 'Gufick'
        VLAD = 'VLAD', 'Vlad'
        VOVA = 'VOVA', 'Vova'
        MAX = 'MAX', 'Max'

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="the_task"
    )

    profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="responsible_person"
    )

    role = models.CharField(max_length=30, choices=Role.choices, default=Role.GUFICK)

    def __str__(self):
        return self.profile.username
    
    def get_delete_url(self):
        return reverse("delete_task_member", kwargs={"pk": self.task.team.id, "taskid": self.task.id, "member_id": self.id})