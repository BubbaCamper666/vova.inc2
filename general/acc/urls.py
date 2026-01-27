from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.user_profile_list, name='user_profile_list'),
    path('profile/<str:username>', views.user_profile, name='user_profile'),
]