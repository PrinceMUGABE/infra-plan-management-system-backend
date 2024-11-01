from rest_framework import serializers

from plannerApp.models import Planner
from projectApp.models import Project
from plannerApp.models import Planner
from userApp.models import User
from funded_project_app.models import FundedProject
from stakeholderApp.models import Stakeholder
from .models import EngineerApplication
from plannedProjectApp.models import PlannedProject
from engineerApp.models import Engineer

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



class EngineerApplicationSerializer(serializers.ModelSerializer):
    created_by = EngineerSerializer(read_only=True)
    project = FundedProjectSerializer(read_only=True)  # Ensure project details are nested correctly

    class Meta:
        model = EngineerApplication
        fields = ['id', 'created_by', 'project', 'status', 'created_at']
        read_only_fields = ['id', 'created_at']
