from django.db import models
from django.core.validators import MinValueValidator
from django.forms import ValidationError
from django.utils import timezone
from django.contrib.auth import get_user_model

class TypeService(models.Model):
    name = models.CharField('Наименование вида услуг', max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Вид услуги'
        verbose_name_plural = 'Виды услуг'

class Service(models.Model):
    FIXED_PRICE = 'fixed'
    FLEXIBLE_PRICE = 'flexible'
    PRICE_TYPE_CHOICES = [
        (FIXED_PRICE, 'Фиксированная цена'),
        (FLEXIBLE_PRICE, 'Гибкая цена'),
    ]

    name = models.CharField('Наименование', max_length=100, default='Новая услуга')
    description = models.TextField('Описание', max_length=750, blank=True)
    photo = models.ImageField('Фото', blank=True, upload_to='services/')
    duration = models.PositiveIntegerField('Длительность (мин)', default=60)
    type_service = models.ForeignKey(
        TypeService, 
        on_delete=models.CASCADE, 
        related_name='services', 
        verbose_name='Вид услуги'
    )
    min_price = models.IntegerField('Минимальная стоимость')
    type_price = models.CharField('Тип цены', max_length=50, choices=PRICE_TYPE_CHOICES)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

class PhotoService(models.Model):
    date_add = models.DateField('Дата добавления', auto_now_add=True)
    photo = models.ImageField('Фото', upload_to='gallery/')
    type_service = models.ForeignKey(
        TypeService, 
        on_delete=models.CASCADE, 
        related_name='gallery_images', 
        verbose_name='Вид услуги'
    )
    
    def __str__(self):
        return f"Фото для {self.type_service.name} ({self.date_add})"

    class Meta:
        verbose_name = 'Фотогалерея'
        verbose_name_plural = 'Фотогалерея'

class Master(models.Model):
    name = models.CharField(max_length=100, verbose_name="ФИО")
    photo = models.ImageField(upload_to='masters/', blank=True, null=True, verbose_name="Фото")
    email = models.EmailField(verbose_name="Почта")
    phone = models.CharField(max_length=20, verbose_name="Телефон")

    def is_available_at(self, datetime, duration_minutes):
        """Проверяет, свободен ли мастер в указанное время"""
        if not hasattr(self, 'schedule'):
            return False
            
        # Проверяем расписание
        if not self.schedule.is_available(datetime, duration_minutes):
            return False
            
        # Проверяем конфликты с записями
        new_end = datetime + timezone.timedelta(minutes=duration_minutes)
        return not self.appointments.filter(
            datetime__lt=new_end,
            datetime_end__gt=datetime,
            status__in=['active', 'completed']
        ).exists()
    
    def _has_conflicting_appointments(self, datetime, service):
        new_end = datetime + timezone.timedelta(minutes=service.duration)
        return self.appointments.filter(
            datetime__lt=new_end, #фильтр беньше
            datetime__gte=datetime - timezone.timedelta(minutes=service.duration), #больше или равно
            status__in=['active', 'completed']
        ).exists()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Мастер'
        verbose_name_plural = 'Мастера'

class MasterSpecialization(models.Model):
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='specializations')
    specialization = models.ForeignKey(TypeService, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.master} - {self.specialization}"

    class Meta:
        verbose_name = 'Специализация мастера'
        verbose_name_plural = 'Специализации Мастеров'
