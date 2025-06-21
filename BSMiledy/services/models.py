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

    def is_available_at(self, datetime, service):
        """Проверяет, свободен ли мастер в указанное время"""
        return not self._has_conflicting_appointments(datetime, service) #проверяем есть ли вообще такие записи которые мешают нам записать человека. если да, возвращаем фолз

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

class Appointment(models.Model):
    ACTIVE = 'active'
    COMPLETED = 'completed'
    CANCELED = 'canceled'
    STATUS_CHOICES = [
        (ACTIVE, 'Активная'),
        (COMPLETED, 'Завершенная'),
        (CANCELED, 'Отмененная'),
    ]

    user = models.ForeignKey(
        get_user_model(), 
        on_delete=models.CASCADE, 
        verbose_name='Пользователь', 
        related_name='appointments'
    )
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Услуга')
    master = models.ForeignKey(Master, on_delete=models.CASCADE, verbose_name='Мастер', related_name='appointments')
    datetime = models.DateTimeField(
        verbose_name='Дата и время', 
        validators=[MinValueValidator(limit_value=timezone.now)]
    )
    comment = models.TextField(verbose_name='Комментарий', max_length=500, blank=True)
    status = models.CharField(
        verbose_name='Статус', 
        max_length=20, 
        choices=STATUS_CHOICES, 
        default=ACTIVE
    )
    created_at = models.DateTimeField(verbose_name='Дата создания записи', auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.service} ({self.datetime})"
    
    def clean(self):
        self._validate_master_specialization()
        self._validate_master_availability()

    def _validate_master_specialization(self):
        if not self.master.specializations.filter(specialization=self.service.type_service).exists():
            raise ValidationError("Этот мастер не оказывает выбранную услугу!")
        
    def _validate_master_availability(self):
        if not self.master.is_available_at(self.datetime, self.service):
            existing = self._get_conflicting_appointment()
            if existing:
                raise ValidationError(self._get_conflict_message(existing))

    def _get_conflicting_appointment(self): #получить конфликтующую запись для вывода ошибки
        return self.master.appointments.filter(
            datetime__lt=self.datetime + timezone.timedelta(minutes=self.service.duration),
            datetime__gte=self.datetime - timezone.timedelta(minutes=self.service.duration),
            status__in=[self.ACTIVE, self.COMPLETED]
        ).first()

    def _get_conflict_message(self, existing):
        return (
            f"Мастер уже занят с {existing.datetime.strftime('%H:%M')} "
            f"до {(existing.datetime + timezone.timedelta(minutes=existing.service.duration)).strftime('%H:%M')}"
        )
        
    def cancel(self):
        if self.is_active:
            self.status = self.CANCELED
            self.save()

    def save(self, *args, **kwargs):
        if self._should_complete():
            self.status = self.COMPLETED
        super().save(*args, **kwargs)

    def _should_complete(self):
        return self.datetime < timezone.now() and self.status == self.ACTIVE

    @property
    def is_active(self):
        return self.status == self.ACTIVE and self.datetime > timezone.now()

    @property
    def is_cancelable(self): # Можно ли отменить запись
        return self.is_active

    @property
    def end_time(self): # Время конца записи 
        return self.datetime + timezone.timedelta(minutes=self.service.duration)

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        ordering = ['-datetime']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'datetime'],
                name='unique_user_datetime',
                violation_error_message="У вас уже есть запись на это время"
            ),
            models.UniqueConstraint(
                fields=['master', 'datetime'],
                name='unique_master_datetime',
                violation_error_message="Мастер уже занят на это время"
            ),
        ]