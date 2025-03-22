from django.contrib import admin
from .models import TypeService, Service, PhotoService

admin.site.register(TypeService)
admin.site.register(Service)
admin.site.register(PhotoService)