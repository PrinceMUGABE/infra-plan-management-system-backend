from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Planner
from .serializers import PlannerSerializer
from django.db import IntegrityError
import logging
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)

# Create a planner
class PlannerCreateView(generics.CreateAPIView):
    queryset = Planner.objects.all()
    serializer_class = PlannerSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        # Validate the serializer
        if not serializer.is_valid():
            # Log validation errors
            logger.error(f"Validation failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Save the planner with the authenticated user as the creator
            planner = serializer.save(created_by=self.request.user)
            
            # Send email notification
            send_mail(
                    subject="Account Created Successfully",
                    message=f"Dear Engineer,\n\nYour account has been successfully created at Infraplan Management System.\n\nThank you for joining our platform!",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[planner.email],
                    fail_silently=False,
                )

            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except IntegrityError as e:
            if 'email' in str(e):
                error_message = {"email": ["A planner with this email already exists."]}
                logger.error("Validation error: Email must be unique.")
            else:
                error_message = {"detail": "An integrity error occurred."}
                logger.error(f"IntegrityError: {e}")

            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Catch any other unexpected exceptions
            logger.error(f"Unexpected error: {e}")
            return Response(
                {"detail": "An unexpected error occurred. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
            
            

# View all planners
class PlannerListView(generics.ListAPIView):
    queryset = Planner.objects.all()
    serializer_class = PlannerSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
    
    
    

# View planner by ID
class PlannerDetailView(generics.RetrieveAPIView):
    queryset = Planner.objects.all()
    serializer_class = PlannerSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
    

# View planner by email
class PlannerByEmailView(generics.RetrieveAPIView):
    serializer_class = PlannerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        email = self.kwargs['email']
        return generics.get_object_or_404(Planner, email=email)
    
    
    

# Edit planner by ID
class PlannerUpdateView(generics.UpdateAPIView):
    queryset = Planner.objects.all()
    serializer_class = PlannerSerializer
    permission_classes = [permissions.IsAuthenticated]


# Delete planner by ID
class PlannerDeleteView(generics.DestroyAPIView):
    queryset = Planner.objects.all()
    serializer_class = PlannerSerializer
    permission_classes = [permissions.IsAuthenticated]
