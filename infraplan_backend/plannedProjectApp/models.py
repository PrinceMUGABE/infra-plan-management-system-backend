# models.py for plannedProjectApp
from django.db import models
from django.core.exceptions import ValidationError
from projectApp.models import Project
from plannerApp.models import Planner

class PlannedProject(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='planned_projects')
    planned_by = models.ForeignKey(Planner, on_delete=models.CASCADE, related_name='planned_projects')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    duration = models.IntegerField(help_text="Duration in days")
    planned_date = models.DateField()
    cost = models.DecimalField(max_digits=10, decimal_places=2, help_text="Cost of the project plan", default=0)
    location = models.CharField(max_length=255, help_text="Location of the project plan", default='')
    image = models.BinaryField(null=True, blank=True, help_text="Image of the project plan")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('project', 'planned_by')

    def clean(self):
        if PlannedProject.objects.filter(project=self.project, planned_by=self.planned_by).exists():
            raise ValidationError("A planner can plan a project only once.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
