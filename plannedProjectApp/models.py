import logging
from django.db import models
from django.core.exceptions import ValidationError
from projectApp.models import Project
from plannerApp.models import Planner

# Create logger
logger = logging.getLogger(__name__)

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
    # planned_date = models.DateField(default=)
    cost = models.DecimalField(max_digits=10, decimal_places=2, help_text="Cost of the project plan", default=0)
    location = models.CharField(max_length=255, help_text="Location of the project plan", default='')
    image = models.BinaryField(null=True, blank=True, help_text="Image of the project plan")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('project', 'planned_by')

    def clean(self):
        """
        Validation to ensure no duplicate project plans by the same planner for the same project.
        """
        if PlannedProject.objects.filter(project=self.project, planned_by=self.planned_by).exists():
            logger.warning(f"Duplicate planned project attempt by planner {self.planned_by.id} for project {self.project.id}")
            raise ValidationError("A planner can plan a project only once.")
        
    def save(self, *args, **kwargs):
        try:
            self.clean()  # Ensure the unique constraint is validated
            super().save(*args, **kwargs)
            logger.info(f"Planned project saved successfully for project {self.project.id} by planner {self.planned_by.id}")
        except ValidationError as e:
            logger.error(f"Validation error while saving planned project: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error while saving planned project: {str(e)}")
            raise e
