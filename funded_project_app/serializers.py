# serializers.py
from rest_framework import serializers
from .models import PlannedProject
from projectApp.models import Project
from plannerApp.models import Planner
from userApp.models import User
from .models import FundedProject
from stakeholderApp.models import Stakeholder

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




class PlannedProjectSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()
    planned_by = PlannerSerializer()

    class Meta:
        model = PlannedProject
        fields = ['id', 'project', 'planned_by', 'status', 'duration', 'cost', 'location', 'image', 'created_at']


class StakeholderSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Stakeholder
        fields = ['id', 'email', 'address', 'monthly_income', 'created_by', 'created_at']
        read_only_fields = ['created_by', 'created_at']


class FundedProjectSerializer(serializers.ModelSerializer):
    created_by = StakeholderSerializer(read_only=True)
    funded_project = PlannedProjectSerializer(read_only=True)

    class Meta:
        model = FundedProject
        fields = ['id', 'created_by', 'funded_project', 'status', 'created_at']
        read_only_fields = ['created_at']
