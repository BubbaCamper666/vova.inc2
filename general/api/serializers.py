from rest_framework import serializers
from task.models import Task, Team, TeamMember, TaskMember
from chnew.models import Room, RoomMember, Message
from chnew.constants import CHNEW_WS_CHAT_PATH

class TeamSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    members_url = serializers.SerializerMethodField()
    tasks_url = serializers.SerializerMethodField()
    delete_url = serializers.SerializerMethodField()
    class Meta:
        fields = (
            "id",
            "status",
            "title",
            "description",
            "createDate",
            "owner",
            "url",
            "members_url",
            "tasks_url",
            "delete_url",
        )
        
        model = Team

    def get_url(self, obj):
        request = self.context.get("request")
        url = obj.get_absolute_url()
        if request:
            return request.build_absolute_uri(url)
        return url
    
    def get_members_url(self, obj):
        request = self.context.get("request")
        url = obj.get_members_url()
        if request:
            return request.build_absolute_uri(url)
        return url
    
    def get_tasks_url(self, obj):
        request = self.context.get("request")
        url = obj.get_tasks_url()
        if request:
            return request.build_absolute_uri(url)
        return url
    
    def get_delete_url(self, obj):
        request = self.context.get("request")
        url = obj.get_delete_url()
        if request:
            return request.build_absolute_uri(url)
        return url
    
class TeamPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "status",
            "title",
            "description",
        )
        #read_only_fields = ("owner", "createDate", "url",)
        model = Team
        
class TeamPUTSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "status",
            "title",
            "description",
        )
        model = Team

class TeamMemberSerializer(serializers.ModelSerializer):
    delete_url = serializers.SerializerMethodField()
    class Meta:
        fields = (
            "team",
            "profile",
            "role",
            "delete_url"
        )
        model = TeamMember
    def get_delete_url(self, obj):
        request = self.context.get("request")
        url = obj.get_deletion_url()
        if request:
            return request.build_absolute_uri(url)
        return url

class TeamMemberPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "profile",
            "role",
        )
        read_only_fields = ["team"]
        model = TeamMember

class TaskSerializer(serializers.ModelSerializer):
    members_url = serializers.SerializerMethodField()
    delete_url = serializers.SerializerMethodField()
    redact_url = serializers.SerializerMethodField()
    class Meta:
        fields = (
            "status",
            "deadline",
            "title",
            "description",
            "createDate",
            "members_url",
            "delete_url",
            "redact_url",
        )
        model = Task
    def get_members_url(self, obj):
        request = self.context.get("request")
        url = obj.get_members_url()
        if request:
            return request.build_absolute_uri(url)
        return url
    
    def get_delete_url(self, obj):
        request = self.context.get("request")
        url = obj.get_delete_url()
        if request:
            return request.build_absolute_uri(url)
        return url
    
    def get_redact_url(self, obj):
        request = self.context.get("request")
        url = obj.get_redact_url()
        if request:
            return request.build_absolute_uri(url)
        return url
    
class TaskPUTSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "status",
            "deadline",
            "title",
            "description",
        )
        model = Task

class TaskPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "status",
            "deadline",
            "title",
            "description",
        )
        model = Task
        
class TaskMemberSerializer(serializers.ModelSerializer):
    delete_url = serializers.SerializerMethodField()
    class Meta:
        fields = (
            "task",
            "profile",
            "role",
            "delete_url",
        )
        model = TaskMember
    def get_delete_url(self, obj):
        request = self.context.get("request")
        url = obj.get_delete_url()
        if request:
            return request.build_absolute_uri(url)
        return url
    
class TaskMemberPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "profile",
            "role",
        )
        read_only_fields = ["team"]
        model = TaskMember

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        view = self.context.get("view")
        if view:
            team_pk = view.kwargs.get("pk")
            if team_pk:
                self.fields["profile"].queryset = TeamMember.objects.filter(
                    team_id=team_pk
                ).distinct()

    def validate_profile(self, user):
        view = self.context["view"]
        team_pk = view.kwargs.get("pk")

        if not TeamMember.objects.filter(team_id=team_pk, profile=user).exists():
            raise serializers.ValidationError(
                "User is not member of the Team."
            )

        return user
    
# CHAT SERIALIZERS

class RoomSerializer(serializers.ModelSerializer):
    chat_url = serializers.SerializerMethodField()
    members_url = serializers.SerializerMethodField()
    delete_url = serializers.SerializerMethodField()
    class Meta:
        fields = (
            "id",
            "owner",
            "title",
            "created_at",
            "chat_url",
            "members_url",
            "delete_url",
        )
        model = Room
        
    def get_chat_url(self, obj):
        request = self.context.get("request")

        path = CHNEW_WS_CHAT_PATH.format(room_id=obj.pk)

        # если request нет (например, сериализация вне view) — вернём относительный путь
        if not request:
            return path

        scheme = "wss" if request.is_secure() else "ws"
        return f"{scheme}://{request.get_host()}{path}"
    
    def get_members_url(self, obj):
        request = self.context.get("request")
        url = obj.get_members_url()
        if request:
            return request.build_absolute_uri(url)
        return url
    
    def get_delete_url(self, obj):
        request = self.context.get("request")
        url = obj.get_delete_url()
        if request:
            return request.build_absolute_uri(url)
        return url
    
class RoomPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "title",
            "created_at",
        )
        model = Room
        
class RoomMemberSerializer(serializers.ModelSerializer):
    delete_url = serializers.SerializerMethodField()
    class Meta:
        fields = (
            "room",
            "user",
            "joined_at",
            "delete_url",
        )
        model = RoomMember
    def get_delete_url(self, obj):
        request = self.context.get("request")
        url = obj.get_delete_url()
        if request:
            return request.build_absolute_uri(url)
        return url

class RoomMemberPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "user",
        )
        read_only_fields = ["room"]
        model = RoomMember
    
    def validate_user(self, user):
        room_id = self.context["view"].kwargs.get("pk")
        # можно .only("owner_id") чтобы не тащить лишнее
        room = Room.objects.only("owner_id").get(pk=room_id)

        if room.owner_id == user.id:
            raise serializers.ValidationError("Владелец комнаты не может быть добавлен как участник.")
        return user