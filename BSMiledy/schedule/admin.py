from django.contrib import admin
from .models import Schedule, DayOff

class DayOffInline(admin.TabularInline):
    model = DayOff
    extra = 1

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('master', 'default_start', 'default_end')
    inlines = [DayOffInline]
    list_filter = ('master',)

@admin.register(DayOff)
class DayOffAdmin(admin.ModelAdmin):
    list_display = ('schedule', 'date', 'start_time', 'end_time', 'reason')
    list_filter = ('reason', 'date')
    date_hierarchy = 'date'