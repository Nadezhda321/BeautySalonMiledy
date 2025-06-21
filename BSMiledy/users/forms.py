from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Client
from django import forms
from django.utils.translation import gettext_lazy as _
import re
from django.utils import timezone
from datetime import timedelta

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label=_("Email"), widget=forms.EmailInput(attrs={'autocomplete': 'email'}))
    first_name = forms.CharField(label=_("Имя"), max_length=150)
    last_name = forms.CharField(label=_("Фамилия"), max_length=150)
    phone = forms.CharField(label=_("Номер телефона"), max_length=20)
    birth_date = forms.DateField(label=_("Дата рождения"), widget=forms.DateInput(attrs={'type': 'date'}))
    consent_pd = forms.BooleanField(label=_("Согласие на обработку ПД"), required=True)
    
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        # Удаляем ВСЕ нецифровые символы
        cleaned_phone = re.sub(r'\D', '', phone)
        
        # Проверяем что номер содержит 11 цифр и начинается с 7 или 8
        if len(cleaned_phone) != 11 or not cleaned_phone.startswith(('7', '8')):
            raise ValidationError(
                "Введите 11-значный номер телефона, начинающийся с 7 или 8. "
                "Пример: 79085093814 или 89085093814"
            )
        return '+7' + cleaned_phone[1:]  # Всегда сохраняем в формате +7XXXXXXXXXX
    
    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        min_age_date = timezone.now().date() - timedelta(days=365*16)
        if birth_date > min_age_date:
            raise ValidationError(
                "Оказание услуг лицам младше 16-ти лет допускается только с разрешения родителей"
            )
        return birth_date
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Настройка минимальной длины пароля
        self.fields['password1'].help_text = "Пароль должен содержать минимум 8 символов, включая буквы и цифры."
        
        # Добавляем маску для телефона
        self.fields['phone'].widget.attrs.update({
            'placeholder': '+7 (XXX) XXX-XX-XX',
            'inputmode': 'tel'  # Для мобильных устройств
        })
        
    class Meta:
        model = Client
        fields = ('email', 'first_name', 'last_name', 'phone', 'birth_date', 'password1', 'password2', 'consent_pd')