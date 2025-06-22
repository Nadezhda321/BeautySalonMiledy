from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Client
from .forms import RegisterForm

class CustomUserAdmin(UserAdmin):
   
    add_form = RegisterForm
   
    ordering = ('email',)  
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone', 'birth_date')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
  
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone', 'birth_date', 'password1', 'password2', 'consent_pd'),
        }),
    )

admin.site.register(Client, CustomUserAdmin)