from rest_framework.response import Response
from django.http import Http404
from django.urls import reverse


from rest_framework import generics, mixins
from rest_framework.views import APIView

from task.models import Team, TeamMember
from . import serializers 
from rest_framework.permissions import IsAuthenticated

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.pagination import PageNumberPagination
class MyStandartPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'p-size'
    max_page_size = 10
    
class Welcome(APIView):
    permission_classes = [IsAuthenticated]
    
    def linky(self, request):
        fixed_path = reverse("teamlist")
        full_url = request.build_absolute_uri(fixed_path)
        return full_url

    def get(self, request):
        return Response({
            "WELCOME": "WELCOME",
            "teamlist": self.linky(request),
        })

class Teamlist(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.TeamSerializer
    
    def get_queryset(self):
        return Team.objects.filter(owner=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.TeamPOSTSerializer
        return serializers.TeamSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    #QOL
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'status']
    search_fields = ['title']
    ordering = ['title'] # default ordering
    ordering_fields = ['title', 'status', 'createDate']

    #pagination
    pagination_class = MyStandartPagination

class TeamDetail(APIView):
    serializer_class = serializers.TeamSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Team.objects.get(pk=pk, owner=self.request.user)
        except Team.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        team = self.get_object(pk)
        seriaizer = serializers.TeamSerializer(team, context={"request": request})
        return Response(seriaizer.data)
    
    def put(self, request, pk):
        team = self.get_object(pk)
        serializer = serializers.TeamPUTSerializer(team, data=request.data, partial=True, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, pk):
        team = self.get_object(pk)
        team.delete()
        return Response(status=204)
        
class TeamMemberList(generics.ListCreateAPIView):
    serializer_class = serializers.TeamMemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        kwarg = self.kwargs.get("pk")
        return TeamMember.objects.filter(team=kwarg)
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return serializers.TeamMemberPOSTSerializer
        return serializers.TeamMemberSerializer
    
    def perform_create(self, serializer):
        kwarg = self.kwargs.get("pk")
        serializer.save(team_id=kwarg)

class TeamMemberDelete(generics.DestroyAPIView):
    serializer_class = serializers.TeamMemberSerializer
    permission_classes = [IsAuthenticated]

    lookup_url_kwarg = "member_id"

    def get_queryset(self):
        team_pk = self.kwargs["pk"]
        return TeamMember.objects.filter(team_id=team_pk)

