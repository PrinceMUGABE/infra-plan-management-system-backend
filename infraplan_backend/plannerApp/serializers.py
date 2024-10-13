# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Planner

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone', 'role', 'created_at']
        read_only_fields = ['id', 'created_at']

class PlannerSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Planner
        fields = ['id', 'created_by', 'email', 'address', 'certificate', 'no_experience', 'created_at']
        read_only_fields = ['created_by', 'created_at']

    def validate_certificate(self, value):
        # Ensure the file is a PDF and does not exceed 5MB
        if not value.name.endswith('.pdf'):
            raise serializers.ValidationError("Certificate must be a PDF file.")
        if value.size > 5 * 1024 * 1024:  # 5MB limit
            raise serializers.ValidationError("Certificate file size must not exceed 5MB.")
        return value
