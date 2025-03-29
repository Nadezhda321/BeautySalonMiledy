from django.shortcuts import render
from django.contrib.auth.decorators import login_required




@login_required #помечаем как требующую логина пользователя
def profile(request):
    return render(request, 'users/profile.html')