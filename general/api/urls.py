from django.urls import path, re_path, include
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('token/', obtain_auth_token),
    
    path("", views.Welcome.as_view(), name="welcome"),
    path("auth/", include("rest_framework.urls")),
    
    path('team/<uuid:pk>/task/', views.TaskList.as_view(), name="tasklist"),
    path('team/<uuid:pk>/task/<int:taskid>/redact/', views.TaskRedact.as_view(), name="taskredact"),
    path('team/<uuid:pk>/task/<int:taskid>/delete/', views.TaskDelete.as_view(), name="taskdelete"),
    path("team/<uuid:pk>/task/<int:taskid>/members/", views.TaskMemberList.as_view(), name="taskmembers"),
    path("team/<uuid:pk>/task/<int:taskid>/members/<int:member_id>/delete/", views.TaskMemberDelete.as_view(), name="delete_task_member"),
    
    path('team/', views.Teamlist.as_view(), name="teamlist"),
    path('team/create/', views.TeamCreate.as_view(), name="teamcreate"),
    path('team/<uuid:pk>/', views.TeamDetail.as_view(), name="teamdetail"),
    path('team/<uuid:pk>/delete/', views.TeamDelete.as_view(), name="teamdelete"),
    path("team/<uuid:pk>/members/<int:member_id>/delete/", views.TeamMemberDelete.as_view(), name="delete_team_member"),
    path('team/<uuid:pk>/members/', views.TeamMemberList.as_view(), name="teammembers"),
    

    
]   
