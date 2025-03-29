from django.shortcuts import render
from .models import Service

def services_home(request):
    service = Service.objects.order_by('name')
    return render(request, 'services/services_home.html', {'service': service})