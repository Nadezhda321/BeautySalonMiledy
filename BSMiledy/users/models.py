from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class Client(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=False)
    last_name = models.CharField(_('last name'), max_length=150, blank=False)
    phone = models.CharField(_('phone number'), max_length=20)  # Увеличьте до 20 символов
    birth_date = models.DateField(_('birth date'), null=True, blank=False)
    consent_pd = models.BooleanField(_('consent to personal data processing'), default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'birth_date']