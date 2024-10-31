from rest_framework import serializers
from .models import EngineerApplication
from engineerApp.serializers import EngineerSerializer
from funded_project_app.serializers import FundedProjectSerializer

class EngineerApplicationSerializer(serializers.ModelSerializer):
    created_by = EngineerSerializer(read_only=True)
    project = FundedProjectSerializer(read_only=True)

    class Meta:
        model = EngineerApplication
        fields = ['id', 'created_by', 'project', 'status', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate(self, data):
        if EngineerApplication.objects.filter(
            created_by=self.context['request'].user.engineer, 
            project=data['project']
        ).exists():
            raise serializers.ValidationError("You have already applied to this project.")
        return data
