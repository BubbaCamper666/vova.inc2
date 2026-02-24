from django.contrib import admin

from chnew.models import Room, RoomMember, Message

admin.site.register(Room)
admin.site.register(RoomMember)
admin.site.register(Message)