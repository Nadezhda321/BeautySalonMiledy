from django.shortcuts import render
from .models import Service, PhotoService, TypeService

def services_home(request):
    service = Service.objects.order_by('name')
    return render(request, 'services/services_home.html', {'service': service})

def gallery(request):
    photos = PhotoService.objects.all().select_related('type_service')
    services = TypeService.objects.all()
    
    context = {
        'photos': photos,
        'services': services
    }
    return render(request, 'services/gallery.html', context)