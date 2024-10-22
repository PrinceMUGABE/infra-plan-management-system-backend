from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Stakeholder(models.Model):
    email = models.EmailField(unique=True, max_length=30)
    address = models.TextField()
    monthly_income = models.DecimalField(max_digits=30, decimal_places=2)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stakeholders')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
