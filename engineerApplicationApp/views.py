from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import EngineerApplication
from .serializers import EngineerApplicationSerializer
from engineerApp.models import Engineer
from funded_project_app.models import FundedProject

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_application(request):
    try:
        engineer = Engineer.objects.get(created_by=request.user)
        project_id = request.data.get('project_id')
        
        # Fetch the funded project
        project = FundedProject.objects.get(id=project_id)
        
        # Check if the funded project is accepted
        if project.status != 'accepted':
            return Response(
                {"error": "Only accepted projects can receive applications."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if the engineer has already applied for this project
        existing_application = EngineerApplication.objects.filter(created_by=engineer, project=project).first()
        if existing_application:
            return Response(
                {"error": "You have already applied for this project."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if the project already has an accepted application
        if EngineerApplication.objects.filter(project=project, status='accepted').exists():
            return Response(
                {"error": "This project has already accepted an application. No further applications are allowed."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create a new application if all checks pass
        application = EngineerApplication(created_by=engineer, project=project)
        application.save()
        
        # Serialize and log the application data
        serializer = EngineerApplicationSerializer(application)
        print(serializer.data)  # Log output for the terminal
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    except Engineer.DoesNotExist:
        return Response({"error": "Engineer profile not found for this user."}, status=status.HTTP_404_NOT_FOUND)
    except FundedProject.DoesNotExist:
        return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    
    
    
       

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_application_by_id(request, application_id):
    try:
        application = EngineerApplication.objects.get(id=application_id)
        serializer = EngineerApplicationSerializer(application)
        print(serializer.data)  # Log output for the terminal
        return Response(serializer.data, status=status.HTTP_200_OK)
    except EngineerApplication.DoesNotExist:
        return Response({"error": "Application not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_applications(request):
    applications = EngineerApplication.objects.all()
    serializer = EngineerApplicationSerializer(applications, many=True)
    print(serializer.data)  # Log output for the terminal
    return Response(serializer.data, status=status.HTTP_200_OK)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_applications_for_engineer(request):
    try:
        # Attempt to retrieve the Engineer associated with the current user
        engineer = Engineer.objects.get(created_by=request.user)
    except Engineer.DoesNotExist:
        # Return a 404 response if the Engineer does not exist
        print("\n\n Engineer not found.\n\n")
        return Response({"detail": "Engineer not found."}, status=status.HTTP_404_NOT_FOUND)

    # If the engineer is found, retrieve the associated applications
    applications = EngineerApplication.objects.filter(created_by=engineer)
    serializer = EngineerApplicationSerializer(applications, many=True)

    print(serializer.data)  # Log output for the terminal
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_application_status(request, application_id):
    status = request.data.get('status')
    if status not in ['pending', 'accepted', 'rejected']:
        return Response({"error": "Invalid status value"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        application = EngineerApplication.objects.get(id=application_id)
        application.status = status
        application.save()
        serializer = EngineerApplicationSerializer(application)
        print(serializer.data)  # Log output for the terminal
        return Response(serializer.data, status=status.HTTP_200_OK)
    except EngineerApplication.DoesNotExist:
        return Response({"error": "Application not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_application(request, application_id):
    try:
        application = EngineerApplication.objects.get(id=application_id)
        application.delete()
        print({"message": "Application deleted"})  # Log output for the terminal
        return Response({"message": "Application deleted"}, status=status.HTTP_204_NO_CONTENT)
    except EngineerApplication.DoesNotExist:
        return Response({"error": "Application not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def accept_application(request, application_id):
    try:
        application = EngineerApplication.objects.get(id=application_id)
        application.status = 'accepted'
        application.save()
        serializer = EngineerApplicationSerializer(application)
        print(serializer.data)  # Log output for the terminal
        return Response(serializer.data, status=status.HTTP_200_OK)
    except EngineerApplication.DoesNotExist:
        return Response({"error": "Application not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def reject_application(request, application_id):
    try:
        application = EngineerApplication.objects.get(id=application_id)
        application.status = 'rejected'
        application.save()
        serializer = EngineerApplicationSerializer(application)
        print(serializer.data)  # Log output for the terminal
        return Response(serializer.data, status=status.HTTP_200_OK)
    except EngineerApplication.DoesNotExist:
        return Response({"error": "Application not found"}, status=status.HTTP_404_NOT_FOUND)
