from rest_framework import permissions
from task.models import Team, TeamMember, Task, TaskMember
from chnew.models import Room, RoomMember

class IsSuperVLAD(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.status == "SUPERVLAD"
    
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
    
class IsOwnerForParentTeam(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        team_pk = view.kwargs.get("pk")
        if not team_pk:
            return False
        return (Team.objects.filter(pk=team_pk, owner=request.user).exists())
    
class isOwnerForParentRoom(permissions.BasePermission):
    def has_permission(self, request, view):
        room_pk = view.kwargs.get("pk")
        if not room_pk:
            return False
        return (Room.objects.filter(pk=room_pk, owner=request.user).exists())

class IsOwnerOrMember(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
    
    def has_object_permission(self, request, view, obj):    
        if request.method in permissions.SAFE_METHODS:
            return TeamMember.objects.filter(team=obj, profile=request.user).exists() or obj.owner == request.user
        else:
            if obj.owner == request.user:
                return True
            return False
        
class IsOwnerOrMemberLIST(permissions.BasePermission):
    def has_permission(self, request, view):
        team_pk = view.kwargs.get("pk")
        if not team_pk:
            return False

        if request.method in permissions.SAFE_METHODS:
            return (
                Team.objects.filter(pk=team_pk, owner=request.user).exists() or
                TeamMember.objects.filter(team_id=team_pk, profile=request.user).exists()
            )
        
        return Team.objects.filter(pk=team_pk, owner=request.user).exists()