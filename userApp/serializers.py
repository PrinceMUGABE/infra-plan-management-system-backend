from rest_framework import serializers
from .models import User
import re

from rest_framework import serializers
from .models import User
import re

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone', 'role', 'password', 'confirm_password', 'created_at']

    def validate_password(self, value):
        if value is not None:
            if len(value) < 8:
                raise serializers.ValidationError("Password must be at least 8 characters long")
            if not re.search(r'[A-Z]', value):
                raise serializers.ValidationError("Password must contain at least one uppercase letter")
            if not re.search(r'[a-z]', value):
                raise serializers.ValidationError("Password must contain at least one lowercase letter")
            if not re.search(r'[0-9]', value):
                raise serializers.ValidationError("Password must contain at least one number")
            if not re.search(r'[@$!%*#?&]', value):
                raise serializers.ValidationError("Password must contain at least one special character")
        return value

    def validate(self, data):
        if 'password' in data and 'confirm_password' in data:
            if data['password'] != data['confirm_password']:
                raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        user = User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data['phone'],
            role=validated_data['role'],
            password=validated_data['password'],
        )
        return user


    def update(self, instance, validated_data):
        # If password is present, handle it
        if 'password' in validated_data:
            validated_data.pop('confirm_password', None)  # Pop confirm password
            instance.set_password(validated_data['password'])  # Set new password

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
