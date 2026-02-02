from rest_framework.response import Response
from django.http import Http404


from rest_framework import generics
from rest_framework.views import APIView

from task.models import Team
from .serializers import TeamSerializer, TeamPOSTSerializer, TeamPUTSerializer
from rest_framework.permissions import IsAuthenticated

class Teamlist(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    #queryset = Team.objects.filter(owner=owner)
    serializer_class = TeamSerializer
    
    def get_queryset(self):
        return Team.objects.filter(owner=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TeamPOSTSerializer
        return TeamSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TeamDetail(APIView):
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return Team.objects.get(pk=pk, owner=self.request.user)
        except Team.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        team = self.get_object(pk)
        seriaizer = TeamSerializer(team)
        return Response(seriaizer.data)
    
    def put(self, request, pk):
        team = self.get_object(pk)
        serializer = TeamPUTSerializer(team, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, pk):
        team = self.get_object(pk)
        team.delete()
        return Response(status=204)
        
    