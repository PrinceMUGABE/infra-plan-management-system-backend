from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Planner
from .serializers import PlannerSerializer
from django.db import IntegrityError
import logging

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
            # Log the validation errors
            logger.error(f"Validation failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Save the planner with the authenticated user as the creator
            serializer.save(created_by=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            # If the user already has a planner, return a validation error
            logger.error("User already has a planner.")
            return Response(
                {"detail": "You have already created a planner."},
                status=status.HTTP_400_BAD_REQUEST
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
