# serializers.py
from rest_framework import serializers
from .models import Engineer
from django.contrib.auth import get_user_model

User = get_user_model()

# User serializer to retrieve user info (like in Planner)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone', 'role', 'created_at']
        read_only_fields = ['id', 'created_at']

# Engineer Serializer
class EngineerSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)  # Display user info

    class Meta:
        model = Engineer
        fields = ['id', 'created_by', 'email', 'address', 'no_experience', 'certificate', 'created_at']
        read_only_fields = ['created_by', 'created_at']

    # Validating certificate file (PDF and max size 5MB)
    def validate_certificate(self, value):
        if value and not value.name.endswith('.pdf'):
            raise serializers.ValidationError("Certificate must be a PDF file.")
        if value and value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Certificate size must not exceed 5MB.")
        return value
