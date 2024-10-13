# models.py

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Project(models.Model):
    STATUS_CHOICES = [
        ('un_planned', 'Un Planned'),
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    field = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='un_planned')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # If project already exists, ensure status transition rules
        if self.pk:
            previous = Project.objects.get(pk=self.pk)
            if previous.status == 'completed' and self.status != 'completed':
                raise ValidationError('Cannot change status of a completed project.')
            if previous.status == 'planned' and self.status == 'completed':
                raise ValidationError('Cannot skip directly to completed from un_planned.')
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.field
