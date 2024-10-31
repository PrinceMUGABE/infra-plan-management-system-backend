from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ValidationError  # Import ValidationError
from funded_project_app.models import FundedProject
from engineerApp.models import Engineer

class EngineerApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    created_by = models.ForeignKey(Engineer, on_delete=models.CASCADE, related_name="applications")
    project = models.ForeignKey(FundedProject, on_delete=models.CASCADE, related_name="applications")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('created_by', 'project')

    def save(self, *args, **kwargs):
        if not self.created_by or not self.project:
            raise ValidationError("Engineer and project must be specified.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Application by {self.created_by.email} for project {self.project.id}"
