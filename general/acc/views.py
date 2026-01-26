from django.shortcuts import render
from django.contrib.auth.models import User
from .models import UserProfile

def user_profile(request, username):
    return render(request, 'acc/user_profile.html', {'username': username})

def user_profile_list(request):
    users = UserProfile.objects.all()
    
    return render(request, 'acc/user_profile_list.html', {'users': users}) # TEMPLATE MISSING!