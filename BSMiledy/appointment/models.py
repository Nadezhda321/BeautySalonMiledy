from django.db import models
from django.contrib.auth import get_user_model
from services.models import Service, Master
from django.utils import timezone

class Appointment(models.Model):
    ACTIVE = 'active'
    COMPLETED = 'completed'
    CANCELED = 'canceled'
    STATUS_CHOICES = [
        (ACTIVE, 'Активная'),
        (COMPLETED, 'Завершенная'),
        (CANCELED, 'Отмененная'),
    ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='appointments')
    datetime = models.DateTimeField()
    comment = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)

    datetime_end = models.DateTimeField()

    def save(self, *args, **kwargs):
        if self.datetime and self.service:
            self.datetime_end = self.datetime + timezone.timedelta(
                minutes=self.service.duration
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.service} ({self.datetime})"

    class Meta:
        ordering = ['-datetime']
        constraints = [
            models.UniqueConstraint(
                fields=['master', 'datetime'],
                name='unique_master_datetime'
            ),
            models.UniqueConstraint(
                fields=['user', 'datetime'],
                name='unique_user_datetime'
            ),
        ]
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'