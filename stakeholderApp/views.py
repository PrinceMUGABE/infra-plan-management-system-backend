from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Stakeholder
from .serializers import StakeholderSerializer
from rest_framework.exceptions import ValidationError
import logging
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)
# Create a Stakeholder
from rest_framework.response import Response
from rest_framework import status

class StakeholderCreateView(generics.CreateAPIView):
    serializer_class = StakeholderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Extract data from request
        email = request.data.get('email')
        address = request.data.get('address')
        monthly_income = request.data.get('monthly_income')

        # Initialize an empty list to collect error messages
        error_messages = []

        # Check if the user already has a stakeholder
        if Stakeholder.objects.filter(created_by=request.user).exists():
            error_msg = "You have already created a stakeholder account."
            logger.error(error_msg)
            error_messages.append(error_msg)

        # Validate the email
        if Stakeholder.objects.filter(email=email).exists():
            error_msg = "A stakeholder with this email already exists."
            logger.error(error_msg)
            error_messages.append(error_msg)

        # Validate the monthly income
        if monthly_income is not None and (float(monthly_income) <= 0):
            error_msg = "Monthly income must be a positive value."
            logger.error(error_msg)
            error_messages.append(error_msg)

        # If there are any error messages, raise a ValidationError
        if error_messages:
            raise ValidationError({"detail": error_messages})

        # If no errors, proceed to create the stakeholder
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        stakeholder = serializer.save(created_by=request.user)
        
        # Send email notification
        send_mail(
                    subject="Account Created Successfully",
                    message=f"Dear Engineer,\n\nYour account has been successfully created at Infraplan Management System.\n\nThank you for joining our platform!",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[stakeholder.email],
                    fail_silently=False,
                )


        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
    
    
    

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
