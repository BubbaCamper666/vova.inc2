from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import User

def user_profile(request, username):
    user = get_object_or_404(User, username=username)

    return render(request, 'acc/us_pro.html', {'user': user})

def user_profile_list(request):
    users = User.objects.all()
    
    return render(request, 'acc/us_pro_list.html', {'users': users})