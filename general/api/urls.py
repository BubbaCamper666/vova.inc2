from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('team/', views.Teamlist.as_view(), name="teamlist")
]