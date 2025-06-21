from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Client
from .forms import RegisterForm

class CustomUserAdmin(UserAdmin):
    # Указываем нашу кастомную форму для добавления пользователя
    add_form = RegisterForm
    # Убираем ссылки на username и заменяем на email
    ordering = ('email',)  # Сортировка по email вместо username
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    
    # Обновляем fieldsets для админки
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone', 'birth_date')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Обновляем add_fieldsets для формы создания пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone', 'birth_date', 'password1', 'password2', 'consent_pd'),
        }),
    )

# Регистрируем нашу модель с кастомным админ-классом
admin.site.register(Client, CustomUserAdmin)