from rest_framework import serializers
from task.models import Task, Team, TeamMember, TaskMember

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