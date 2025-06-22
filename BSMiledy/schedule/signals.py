from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Master, Schedule

@receiver(post_save, sender=Master)
def create_master_schedule(sender, instance, created, **kwargs):
    if created:
        Schedule.objects.create(master=instance)