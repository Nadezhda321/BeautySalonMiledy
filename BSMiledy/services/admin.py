from django.contrib import admin
from .models import TypeService, Service, PhotoService, Master, MasterSpecialization


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'type_service', 'min_price')


@admin.register(PhotoService)
class PhotoServiceAdmin(admin.ModelAdmin):
    list_display = ('type_service', 'date_add')
    list_filter = ('type_service',)


class MasterSpecializationInline(admin.TabularInline):
    model = MasterSpecialization
    extra = 1
    autocomplete_fields = ['specialization']


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    inlines = [MasterSpecializationInline]


@admin.register(TypeService)
class TypeServiceAdmin(admin.ModelAdmin):
    search_fields = ['name']