from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path("", views.Welcome.as_view(), name="welcome"),
    path("auth/", include("rest_framework.urls")),
    path('team/<uuid:pk>/', views.TeamDetail.as_view(), name="teamdetail"),
    path('team/', views.Teamlist.as_view(), name="teamlist"),
    path("teammembers/<uuid:pk>/delete/<int:member_id>/", views.TeamMemberDelete.as_view(), name="delete_team_member"),
    path('teammembers/<uuid:pk>/', views.TeamMemberList.as_view(), name="teammembers")
    
]   