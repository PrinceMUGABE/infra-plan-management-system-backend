# funded_project_app/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from projectApp.models import Project
from plannedProjectApp.models import PlannedProject
from stakeholderApp.models import Stakeholder

class FundedProject(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    created_by = models.ForeignKey(Stakeholder, on_delete=models.CASCADE, related_name='funded_projects')
    funded_project = models.ForeignKey(PlannedProject, on_delete=models.CASCADE, related_name='funded_projects')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('created_by', 'funded_project')  # Ensures only one funding per user per project

    # def clean(self):
    #     if not self.created_by.role in ['stakeholder', 'admin']:
    #         raise ValidationError("Only users with Stakeholder or Admin role can fund a project.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
