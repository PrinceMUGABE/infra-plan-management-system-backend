from rest_framework import serializers
from .models import Stakeholder
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone', 'role', 'created_at']
        read_only_fields = ['id', 'created_at']

        



class StakeholderSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Stakeholder
        fields = ['id', 'email', 'address', 'monthly_income', 'created_by', 'created_at']
        read_only_fields = ['created_by', 'created_at']

    def validate_email(self, value):
        """
        Validate that the email is unique, but allow the same email for the current stakeholder being updated.
        """
        # Get the stakeholder ID from the context (passed during update)
        stakeholder_id = self.instance.id if self.instance else None

        # Check if another stakeholder with the same email exists, excluding the current stakeholder
        if Stakeholder.objects.filter(email=value).exclude(id=stakeholder_id).exists():
            raise ValidationError("A stakeholder with this email already exists.")
        
        return value

    def validate_monthly_income(self, value):
        """
        Validate that monthly income is a positive number.
        """
        if value <= 0:
            raise ValidationError("Monthly income must be a positive value.")
        return value
