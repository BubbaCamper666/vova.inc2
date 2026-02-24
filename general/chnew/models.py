from django.conf import settings
from django.db import models
from django.urls import reverse
from acc.models import User

User = settings.AUTH_USER_MODEL

class Room(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="room_owner", null=True, blank=True)
    title = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def get_members_url(self):
        return reverse("api:roommembers", kwargs={"pk": self.pk})
    
    def get_delete_url(self):
        return reverse("api:roomdelete", kwargs={"pk": self.pk})
    
class RoomMember(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="room_memberships")
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("room", "user")
        
    def get_delete_url(self):
        return reverse("api:delete_room_member", kwargs={"pk": self.room.pk, "member_id": self.pk})

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)