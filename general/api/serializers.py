from rest_framework import serializers
from task.models import Task, Team, TeamMember, TaskMember

class TeamSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    members_url = serializers.SerializerMethodField()
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
