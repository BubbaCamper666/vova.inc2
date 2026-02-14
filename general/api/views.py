from rest_framework.response import Response
from django.http import Http404
from django.urls import reverse


from rest_framework import generics, mixins
from rest_framework.views import APIView

from task.models import Team, TeamMember, Task, TaskMember
from . import serializers 
from . import permissions
from rest_framework.permissions import IsAuthenticated

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from django.db.models import Q

from rest_framework.pagination import PageNumberPagination
class MyStandartPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'p-size'
    max_page_size = 10

import uuid
from django.utils.timezone import now

class Welcome(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_teamlist_url(self, request):
        fixed_path = reverse("teamlist")
        full_url = request.build_absolute_uri(fixed_path)
        return full_url
    
    def get_teamcreate_url(self, request):
        fixed_path = reverse("teamcreate")
        full_url = request.build_absolute_uri(fixed_path)
        return full_url

    def get(self, request):
        return Response({
            "WELCOME": "WELCOME",
            "teamlist": self.get_teamlist_url(request),
            "teamcreate": self.get_teamcreate_url(request),
        })

class Teamlist(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.TeamSerializer
    
    def get_queryset(self):
        if self.request.user.status == "VLAD": 
            return Team.objects.filter(owner=self.request.user)
        elif self.request.user.status == "SUPERVLAD": 
            return Team.objects.filter(
                Q(users_team__profile=self.request.user) | #query1
                Q(owner=self.request.user) #query2
            ).distinct()

    #QOL
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'status']
    search_fields = ['title']
    ordering = ['owner'] # default ordering
    ordering_fields = ['title', 'status', 'createDate']

    #pagination
    pagination_class = MyStandartPagination
    
class TeamCreate(generics.CreateAPIView):
    serializer_class = serializers.TeamPOSTSerializer
    permission_classes = [permissions.IsSuperVLAD]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
class TeamDelete(generics.DestroyAPIView):
    serializer_class = serializers.TeamSerializer
    permission_classes = [permissions.IsOwner]
    
    lookup_url_kwarg = "pk"
    lookup_field = "id"
    
    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return Team.objects.filter(id=pk)

class TeamDetail(APIView):
    serializer_class = serializers.TeamSerializer
    permission_classes = [permissions.IsOwnerOrMember]
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
    permission_classes = [permissions.IsOwnerOrMemberLIST]

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
    permission_classes = [permissions.IsOwnerForParentTeam]

    lookup_url_kwarg = "member_id"
    lookup_field = "id"

    def get_queryset(self):
        team_pk = self.kwargs["pk"]
        return TeamMember.objects.filter(team_id=team_pk)

class TaskList(generics.ListCreateAPIView): 
    permission_classes = [permissions.IsOwnerOrMemberLIST]
    serializer_class = serializers.TaskSerializer
    
    def get_queryset(self):
        pk = self.kwargs.get("pk")
        parentTeam = Team.objects.get(id=pk)
        return Task.objects.filter(team=parentTeam)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.TaskPOSTSerializer
        return serializers.TaskSerializer
    
    def perform_create(self, serializer):
        pk = self.kwargs.get("pk")
        parentTeam = Team.objects.get(id=pk)
        serializer.save(team=parentTeam)


    #QOL
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'status']
    search_fields = ['title']
    ordering = ['status', 'deadline'] # default ordering
    ordering_fields = ['title', 'status', 'createDate', 'deadline']

    #pagination
    pagination_class = MyStandartPagination
    
class TaskRedact(APIView):
    serializer_class = serializers.TaskSerializer
    permission_classes = [permissions.IsOwner] 
    
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return serializers.TaskPUTSerializer
        return serializers.TaskSerializer

    def get_object(self, pk, taskid):
        try:
            return Task.objects.get(pk=taskid, team_id=pk)
        except Task.DoesNotExist:
            raise Http404

    def get(self, request, pk, taskid):
        task = self.get_object(pk, taskid)
        seriaizer = serializers.TaskSerializer(task, context={"request": request})
        return Response(seriaizer.data)
    
    def put(self, request, pk, taskid):
        task = self.get_object(pk, taskid)
        serializer = serializers.TaskPUTSerializer(task, data=request.data, partial=True, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
class TaskDelete(generics.DestroyAPIView):
    serializer_class = serializers.TaskSerializer
    permission_classes = [permissions.IsOwnerForParentTeam]
    
    lookup_url_kwarg = "taskid"
    lookup_field = "id"

    def get_queryset(self):
        team_pk = self.kwargs.get("pk")
        taskid = self.kwargs.get("taskid")
        return Task.objects.filter(team=team_pk, id=taskid)

class TaskMemberList(generics.ListCreateAPIView):
    serializer_class = serializers.TaskMemberSerializer
    permission_classes = [permissions.IsOwnerOrMemberLIST]
    
    #WHILE CREATING MUST BE ABLE TO CHOOSE ONLY FROM TEAM MEMBERS, NOT ALL USERS
    
    def get_queryset(self):
        team_pk = self.kwargs.get("pk")
        return TaskMember.objects.filter(task__team_id=team_pk)
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return serializers.TaskMemberPOSTSerializer
        return serializers.TaskMemberSerializer
    
    def perform_create(self, serializer):
        team_pk = self.kwargs.get("pk")
        taskid = self.kwargs.get("taskid")
        task = Task.objects.get(team_id=team_pk, id=taskid)
        serializer.save(task=task)
    

class TaskMemberDelete(generics.DestroyAPIView):
    serializer_class = serializers.TaskMemberSerializer
    permission_classes = [permissions.IsOwnerForParentTeam]
    
    lookup_url_kwarg = "member_id"
    lookup_field = "id"

    def get_queryset(self):
        team_pk = self.kwargs.get("pk")
        taskid = self.kwargs.get("taskid")
        member_id = self.kwargs.get("member_id")
        return TaskMember.objects.filter(task__team_id=team_pk, task__id=taskid, id=member_id)