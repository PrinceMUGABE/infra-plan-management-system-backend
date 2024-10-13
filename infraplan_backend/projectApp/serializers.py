from rest_framework import serializers
from .models import Project
from userApp.models import User

from django.contrib.auth import get_user_model


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone', 'role', 'created_at']
        read_only_fields = ['id', 'created_at']



class ProjectSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Project
        fields = ['id', 'field', 'description', 'status', 'created_by', 'created_at']
        read_only_fields = ['id', 'created_by', 'created_at']
