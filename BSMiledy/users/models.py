from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

class ClientManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Создает и сохраняет пользователя с указанным email и паролем
        """
        if not email:
            raise ValueError('Пользователь должен иметь email адрес')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создает и сохраняет суперпользователя с указанным email и паролем
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True')
            
        return self.create_user(email, password, **extra_fields)

class Client(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=False)
    last_name = models.CharField(_('last name'), max_length=150, blank=False)
    phone = models.CharField(_('phone number'), max_length=20)
    birth_date = models.DateField(_('birth date'), null=True, blank=False)
    consent_pd = models.BooleanField(_('consent to personal data processing'), default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'birth_date']

    objects = ClientManager()

    def __str__(self):
        return self.email