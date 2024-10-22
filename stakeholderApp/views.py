from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Stakeholder
from .serializers import StakeholderSerializer
from rest_framework.exceptions import ValidationError

# Create a Stakeholder
from rest_framework.response import Response
from rest_framework import status

class StakeholderCreateView(generics.CreateAPIView):
    serializer_class = StakeholderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Check if the user already has a stakeholder
        if Stakeholder.objects.filter(created_by=self.request.user).exists():
            raise ValidationError({"detail": "You have already created a stakeholder account."})

        # If no existing stakeholder, proceed with the creation
        serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            if isinstance(e.detail, dict) and 'detail' in e.detail:
                # Specific error message (e.g., user already has a stakeholder account)
                return Response({'error': e.detail['detail']}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # General error handling
                return Response({'error': 'An error occurred while creating the stakeholder account.'}, status=status.HTTP_400_BAD_REQUEST)


# Get Stakeholder by ID, Update, Delete
class StakeholderDetailView(generics.RetrieveAPIView):
    queryset = Stakeholder.objects.all()
    serializer_class = StakeholderSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Stakeholder, id=self.kwargs['pk'])

# Get Stakeholder by Phone
class StakeholderByPhoneView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, phone):
        stakeholder = get_object_or_404(Stakeholder, phone=phone)
        serializer = StakeholderSerializer(stakeholder)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Get Stakeholder by Email
class StakeholderByEmailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, email):
        stakeholder = get_object_or_404(Stakeholder, email=email)
        serializer = StakeholderSerializer(stakeholder)
        return Response(serializer.data, status=status.HTTP_200_OK)

# List All Stakeholders
class StakeholderListView(generics.ListAPIView):
    queryset = Stakeholder.objects.all()
    serializer_class = StakeholderSerializer
    permission_classes = [IsAuthenticated]

# Update a Stakeholder
from rest_framework.response import Response
from rest_framework import status

class StakeholderUpdateView(generics.UpdateAPIView):
    queryset = Stakeholder.objects.all()
    serializer_class = StakeholderSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Stakeholder, id=self.kwargs['pk'])

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        

# Delete a Stakeholder
class StakeholderDeleteView(generics.DestroyAPIView):
    queryset = Stakeholder.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Stakeholder, id=self.kwargs['pk'])



def validate_email(self, value):
    request = self.context.get('request')  # Access the current request
    stakeholder_id = request.parser_context.get('kwargs').get('pk')  # Get the stakeholder ID from the URL

    # Check for duplicate emails but allow the same email for the current stakeholder
    if Stakeholder.objects.filter(email=value).exclude(id=stakeholder_id).exists():
        raise ValidationError("A stakeholder with this email already exists.")
    return value
