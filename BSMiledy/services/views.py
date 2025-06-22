from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Service, PhotoService, TypeService

def services_home(request):
    services = Service.objects.all().select_related('type_service')
    service_types = TypeService.objects.all()
    
    context = {
        'services': services,
        'service_types': service_types
    }
    return render(request, 'services/services_home.html', context)

def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    return render(request, 'services/service_detail.html', {'service': service})

def gallery(request):
    photos = PhotoService.objects.all().select_related('type_service')
    services = TypeService.objects.all()
    
    context = {
        'photos': photos,
        'services': services
    }
    return render(request, 'services/gallery.html', context)