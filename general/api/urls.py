from django.urls import path, re_path, include
from . import views

urlpatterns = [
    
    path("auth/", include("rest_framework.urls")),
    path('team/<uuid:pk>/', views.TeamDetail.as_view(), name="teamdetail"),
    path('team/', views.Teamlist.as_view(), name="teamlist"),
    
]