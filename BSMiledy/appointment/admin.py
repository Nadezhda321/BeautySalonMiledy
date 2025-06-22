import csv
from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Appointment
from services.models import Master, Service

class FutureAppointmentFilter(admin.SimpleListFilter):
    title = _('Будущие записи')
    parameter_name = 'future'
    
    def lookups(self, request, model_admin):
        return (
            ('yes', _('Только будущие')),
            ('no', _('Только прошедшие')),
        )
    
    def queryset(self, request, queryset):
        now = timezone.now()
        if self.value() == 'yes':
            return queryset.filter(datetime__gte=now)
        if self.value() == 'no':
            return queryset.filter(datetime__lt=now)

def mark_as_completed(modeladmin, request, queryset):
    queryset.update(status='completed')
mark_as_completed.short_description = "Отметить как завершенные"

def mark_as_canceled(modeladmin, request, queryset):
    queryset.update(status='canceled')
mark_as_canceled.short_description = "Отметить как отмененные"

def export_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="appointments.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Пользователь', 'Услуга', 'Мастер', 'Дата и время', 'Статус'])
    
    for obj in queryset:
        writer.writerow([
            obj.user.get_full_name() or obj.user.username,
            obj.service.name,
            obj.master.name,
            obj.datetime.strftime("%d.%m.%Y %H:%M"),
            obj.get_status_display()
        ])
    
    return response
export_to_csv.short_description = "Экспорт в CSV"

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'service_type', 'master', 'formatted_datetime', 'status')
    list_filter = (FutureAppointmentFilter, 'status', 'master', 'service')
    search_fields = ('user__username', 'master__name', 'service__name')
    date_hierarchy = 'datetime'
    ordering = ('-datetime',)
    actions = [mark_as_completed, mark_as_canceled, export_to_csv]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'service', 'master', 'status')
        }),
        ('Дата и время', {
            'fields': ('datetime', 'datetime_end')
        }),
        ('Дополнительно', {
            'fields': ('comment', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'datetime_end')
    
    def service_type(self, obj):
        return obj.service.type_service.name
    service_type.short_description = 'Тип услуги'
    
    def formatted_datetime(self, obj):
        return obj.datetime.strftime("%d.%m.%Y %H:%M")
    formatted_datetime.short_description = 'Дата и время'
    formatted_datetime.admin_order_field = 'datetime'
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "master":
            kwargs["queryset"] = Master.objects.order_by('name')
        if db_field.name == "service":
            kwargs["queryset"] = Service.objects.order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)