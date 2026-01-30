from rest_framework import serializers
from task.models import Task, Team, TeamMember, TaskMember

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "status",
            "title",
            "description",
            "createDate",
            "owner",
        )
        model = Team