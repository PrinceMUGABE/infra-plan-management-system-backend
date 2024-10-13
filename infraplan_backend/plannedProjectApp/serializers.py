# serializers.py

from rest_framework import serializers
from .models import PlannedProject
from projectApp.models import Project
from plannerApp.models import Planner
from userApp.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone', 'role', 'created_at']
        read_only_fields = ['id', 'created_at']


class ProjectSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)  # Include creator information

    class Meta:
        model = Project
        fields = ['id', 'field', 'description', 'status', 'created_by', 'created_at']
        read_only_fields = ['id', 'created_by', 'created_at']


class PlannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planner
        fields = ['id', 'email', 'address', 'no_experience', 'created_at']
        read_only_fields = ['id', 'created_at']



class PlannedProjectSerializer(serializers.ModelSerializer):
    planned_by = PlannerSerializer(read_only=True)  # Include planner details
    project = ProjectSerializer(read_only=True)  # Include project details

    class Meta:
        model = PlannedProject
        fields = ['id', 'project', 'planned_by', 'status', 'duration', 'planned_date', 'cost', 'location', 'image', 'created_at']
        read_only_fields = ['id', 'planned_by', 'created_at']

class PlannedProjectDetailSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()  # Include full project details
    planned_by = PlannerSerializer()  # Include full planner details

    class Meta:
        model = PlannedProject
        fields = '__all__'  # Include all fields for detailed view




from rest_framework import serializers
from .models import PlannedProject

class PlannedProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlannedProject
        fields = ['project', 'planned_by', 'status', 'duration', 'cost', 'location', 'image']  # Fields you allow to post
        extra_kwargs = {
            'project': {'required': True},
            'planned_by': {'required': True},
            'duration': {'required': True},
            'cost': {'required': True},
            'location': {'required': True},
        }
    
    def validate(self, data):
        """
        Perform custom validation for the fields
        """
        if data['duration'] <= 0:
            raise serializers.ValidationError("Duration must be a positive integer.")
        if data['cost'] <= 0:
            raise serializers.ValidationError("Cost must be a positive number.")
        
        return data
    
# progress
