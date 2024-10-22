from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import EngineerSerializer
from .models import Engineer
from django.db import IntegrityError
import logging

logger = logging.getLogger(__name__)

class CreateEngineerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Check if the user already has an engineer
        if Engineer.objects.filter(created_by=request.user).exists():
            logger.error("User already has an engineer.")
            return Response(
                {"detail": "You have already created an engineer."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = EngineerSerializer(data=request.data)

        # Validate serializer data
        if serializer.is_valid():
            try:
                # Save the engineer with the authenticated user as the creator
                serializer.save(created_by=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                logger.error(f"IntegrityError: {serializer.errors}")
                return Response(
                    {"detail": "Engineer with this email already exists."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ListEngineerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        engineers = Engineer.objects.all().order_by('created_at')
        serializer = EngineerSerializer(engineers, many=True)
        return Response(serializer.data)
    
    
    
class RetrieveEngineerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            engineer = Engineer.objects.get(pk=pk)
            serializer = EngineerSerializer(engineer)
            return Response(serializer.data)
        except Engineer.DoesNotExist:
            return Response({"detail": "Engineer not found."}, status=status.HTTP_404_NOT_FOUND)
        
              
        
class RetrieveEngineerByEmailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        email = request.query_params.get('email')
        if email:
            try:
                engineer = Engineer.objects.get(email=email)
                serializer = EngineerSerializer(engineer)
                return Response(serializer.data)
            except Engineer.DoesNotExist:
                return Response({"detail": "Engineer not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"detail": "Email parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    
    
class UpdateEngineerView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            engineer = Engineer.objects.get(pk=pk)
            serializer = EngineerSerializer(engineer, data=request.data, partial=False)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Engineer.DoesNotExist:
            return Response({"detail": "Engineer not found."}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            engineer = Engineer.objects.get(pk=pk)
            serializer = EngineerSerializer(engineer, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Engineer.DoesNotExist:
            return Response({"detail": "Engineer not found."}, status=status.HTTP_404_NOT_FOUND)
        
        
        
        
        
        
class DeleteEngineerView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            engineer = Engineer.objects.get(pk=pk)
            engineer.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Engineer.DoesNotExist:
            return Response({"detail": "Engineer not found."}, status=status.HTTP_404_NOT_FOUND)