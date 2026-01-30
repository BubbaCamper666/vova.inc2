from django.shortcuts import render
from rest_framework import generics
from task.models import Team
from .serializers import TeamSerializer

class Teamlist(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer