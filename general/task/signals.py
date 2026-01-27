from django.db.models.signals import post_save
from .models import Team, Task
from django.dispatch import receiver

@receiver(post_save, sender=Team)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Task.objects.create(team=instance, title="example_task")