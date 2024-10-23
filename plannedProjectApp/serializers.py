# serializers.py
from rest_framework import serializers
from .models import PlannedProject
from projectApp.models import Project
from plannerApp.models import Planner
from userApp.models import User

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


class PlannerSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Planner
        fields = ['created_by', 'address', 'no_experience', 'email']




class PlannedProjectDetailSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()
    planned_by = PlannerSerializer()

    class Meta:
        model = PlannedProject
        fields = '__all__'



class DisplayPlannedProjectSerializer(serializers.ModelSerializer):
    planned_by = PlannerSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = PlannedProject
        fields = ['id', 'project', 'planned_by', 'status', 'duration', 'cost', 'location', 'image', 'created_at']
        read_only_fields = ['id', 'planned_by', 'created_at']


from rest_framework import serializers
from .models import PlannedProject

class PlannedProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlannedProject
        fields = ['project', 'status', 'duration', 'cost', 'location', 'image']
        extra_kwargs = {
            'project': {'required': True},
            'duration': {'required': True},
            'cost': {'required': True},
            'location': {'required': True},
        }

    def validate(self, data):
        """
        Perform custom validation for the fields
        """
        if 'duration' in data and data['duration'] <= 0:
            raise serializers.ValidationError("Duration must be a positive integer.")
        if 'cost' in data and data['cost'] <= 0:
            raise serializers.ValidationError("Cost must be a positive number.")
        
        return data
