from rest_framework import permissions
from task.models import Team, TeamMember, Task, TaskMember

class IsSuperVLAD(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.status == "SUPERVLAD"
    
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
    
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
    pass
        

    
