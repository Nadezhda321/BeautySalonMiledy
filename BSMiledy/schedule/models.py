from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

from services.models import Master

class Schedule(models.Model):
    master = models.OneToOneField(Master, on_delete=models.CASCADE, related_name='schedule')
    default_start = models.TimeField(default='09:00', verbose_name="Начало рабочего дня")
    default_end = models.TimeField(default='18:00', verbose_name="Конец рабочего дня")
    lunch_start = models.TimeField(default='13:00', verbose_name="Начало перерыва")
    lunch_end = models.TimeField(default='14:00', verbose_name="Конец перерыва")

    def is_available(self, datetime, duration_minutes):
        time = datetime.time()
        date = datetime.date()
        
        # Проверяем рабочий день
        if not self.is_working_day(date):
            return False
            
        # Проверяем рабочие часы
        if not (self.default_start <= time <= self.default_end):
            return False
            
        # Проверяем перерыв
        if self.lunch_start <= time < self.lunch_end:
            return False
            
        # Проверяем отсутствия/отпуска
        for day_off in self.days_off.filter(date=date):
            if day_off.start_time is None or day_off.end_time is None:
                return False  # Весь день нерабочий
                
            if (day_off.start_time <= time < day_off.end_time) or \
               (time <= day_off.start_time and (time + timezone.timedelta(minutes=duration_minutes)).time() > day_off.start_time):
                return False
                
        return True
        
    def is_working_day(self, date):
        # Проверяем глобальные нерабочие дни (для всех мастеров)
        if DayOff.objects.filter(date=date, reason='day_off', schedule__master__isnull=False).exists():
            return False
            
        # Здесь можно добавить проверку выходных дней, если нужно
        return True

    def __str__(self):
        return f"Расписание для {self.master.name}"

class DayOff(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='days_off')
    date = models.DateField(verbose_name="Дата отсутствия")
    start_time = models.TimeField(null=True, blank=True, verbose_name="Начало отсутствия")
    end_time = models.TimeField(null=True, blank=True, verbose_name="Конец отсутствия")
    reason = models.CharField(max_length=100, choices=[
        ('vacation', 'Отпуск'),
        ('absence', 'Отсутствие'),
        ('day_off', 'Нерабочий день')
    ], verbose_name="Причина")

    def __str__(self):
        return f"{self.get_reason_display()} для {self.schedule.master.name} на {self.date}"

    class Meta:
        verbose_name = 'Отсутствие/отпуск'
        verbose_name_plural = 'Отсутствия/отпуска'

