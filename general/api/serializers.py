from rest_framework import serializers
from task.models import Task, Team, TeamMember, TaskMember

class TeamSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    class Meta:
        fields = (
            "id",
            "status",
            "title",
            "description",
            "createDate",
            "owner",
            "url",
        )
        
        model = Team

    def get_url(self, obj):
        request = self.context.get("request")
        url = obj.get_absolute_url()
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