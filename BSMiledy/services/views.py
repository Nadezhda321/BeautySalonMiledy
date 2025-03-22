from django.shortcuts import render

def services_home(request):
    return render(request, 'services/services_home.html')