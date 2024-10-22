# models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Planner(models.Model):
    created_by = models.OneToOneField(User, on_delete=models.CASCADE, related_name='planner')
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255)
    certificate = models.FileField(upload_to='certificates/', blank=False, null=False)
    no_experience = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
