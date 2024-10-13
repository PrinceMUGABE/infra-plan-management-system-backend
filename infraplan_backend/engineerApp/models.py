from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Engineer(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="engineers")
    email = models.EmailField(unique=True)  # Ensures unique email
    address = models.CharField(max_length=255)
    no_experience = models.PositiveIntegerField()  # Number of years of experience
    certificate = models.FileField(upload_to="certificates/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
