# admin.py
from django.contrib import admin
from .models import Schedule, DayOff
from .forms import DayOffForm

class DayOffInline(admin.TabularInline):
    model = DayOff
    form = DayOffForm
    extra = 1
    fields = ('reason', 'date', 'end_date', 'start_time', 'end_time')
    verbose_name_plural = "Периоды отсутствия"

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('master', 'default_start', 'default_end')
    inlines = [DayOffInline]
    list_filter = ('master',)

@admin.register(DayOff)
class DayOffAdmin(admin.ModelAdmin):
    form = DayOffForm
    list_display = ('schedule', 'get_reason_display', 'date', 'end_date', 'start_time', 'end_time')
    list_filter = ('reason', 'date', 'schedule__master')
    date_hierarchy = 'date'
    
    fieldsets = (
        (None, {
            'fields': ('schedule', 'reason')
        }),
        ('Период отсутствия', {
            'fields': ('date', 'end_date'),
            'description': 'Укажите начальную и конечную даты. Для разового отсутствия укажите одинаковые даты.'
        }),
        ('Время отсутствия', {
            'fields': ('start_time', 'end_time'),
            'description': 'Время, когда мастер недоступен'
        }),
    )