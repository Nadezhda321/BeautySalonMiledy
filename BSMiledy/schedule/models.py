from django.db import models
from django.utils import timezone
from django.db.models import Q
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
        
        if DayOff.objects.filter(
            Q(reason='day_off') & 
            Q(date__lte=date, end_date__gte=date)
        ).exists():
            return False
        
        if not (self.default_start <= time <= self.default_end):
            return False
            
     
        if self.lunch_start <= time < self.lunch_end:
            return False
          
        conflicting_days = self.days_off.filter(
            Q(date__lte=date, end_date__gte=date)
        )
        
        for day_off in conflicting_days:
            if (day_off.start_time <= time < day_off.end_time) or \
            (time <= day_off.start_time and (time + timezone.timedelta(minutes=duration_minutes)).time() > day_off.start_time):
                return False
                
        return True
        
    def is_working_day(self, date):
        if DayOff.objects.filter(
            date__lte=date, 
            end_date__gte=date,
            reason='day_off'
        ).exists():
            return False
        return True

    def __str__(self):
        return f"Расписание для {self.master.name}"
    
    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'

class DayOff(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='days_off')
    date = models.DateField(verbose_name="Начальная дата отсутствия")
    end_date = models.DateField(verbose_name="Конечная дата отсутствия")
    start_time = models.TimeField(default='09:00', verbose_name="Начало отсутствия")
    end_time = models.TimeField(default='18:00', verbose_name="Конец отсутствия")
    reason = models.CharField(max_length=100, choices=[
        ('vacation', 'Отпуск'),
        ('absence', 'Отсутствие'),
        ('day_off', 'Нерабочий день')
    ], verbose_name="Причина")

    def save(self, *args, **kwargs):
        if self.date and self.end_date:
            if self.pk:
                DayOff.objects.filter(
                    schedule=self.schedule,
                    date__range=[self.date, self.end_date],
                    reason=self.reason
                ).exclude(pk=self.pk).delete()
            
            dates_to_create = []
            current_date = self.date
            while current_date <= self.end_date:
                if not DayOff.objects.filter(
                    schedule=self.schedule,
                    date=current_date,
                    reason=self.reason
                ).exists():
                    dates_to_create.append(current_date)
                current_date += timezone.timedelta(days=1)
            
            DayOff.objects.bulk_create([
                DayOff(
                    schedule=self.schedule,
                    date=date,
                    end_date=date,
                    start_time=self.start_time,
                    end_time=self.end_time,
                    reason=self.reason
                ) for date in dates_to_create
            ])
            return
        super().save(*args, **kwargs)

    def __str__(self):
        if self.date == self.end_date:
            return f"{self.get_reason_display()} для {self.schedule.master.name} на {self.date}"
        return f"{self.get_reason_display()} для {self.schedule.master.name} с {self.date} по {self.end_date}"

    class Meta:
        verbose_name = 'Отсутствие/отпуск'
        verbose_name_plural = 'Отсутствия/отпуска'