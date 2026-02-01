from django.shortcuts import render

from rest_framework import generics
from rest_framework.views import APIView

from task.models import Team
from .serializers import TeamSerializer
from rest_framework.permissions import IsAuthenticated

class Teamlist(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    #queryset = Team.objects.filter(owner=owner)
    serializer_class = TeamSerializer
    
    def get_queryset(self):
        return Team.objects.filter(owner=self.request.user)

class TeamDetail(APIView):
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]
