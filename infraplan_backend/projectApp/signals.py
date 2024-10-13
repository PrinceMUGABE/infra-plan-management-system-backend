from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Project
from .views import notify_status_change

@receiver(pre_save, sender=Project)
def log_and_notify_project_changes(sender, instance, **kwargs):
    if instance.pk:
        previous = Project.objects.get(pk=instance.pk)
        if previous.status != instance.status:
            notify_status_change(instance)
