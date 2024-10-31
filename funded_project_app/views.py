import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from .models import FundedProject
from .serializers import FundedProjectSerializer
from stakeholderApp.models import Stakeholder
from plannedProjectApp.models import PlannedProject
from userApp.models import User
from projectApp.models import Project

# Configure the logger
logger = logging.getLogger("funded_project_app")  # Replace with your app's logger name

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_funded_project(request):
    logger.debug("Received request data: %s", request.data)
    
    user = request.user
    assigned_user_id = request.data.get('assigned_user_id')  # ID of the user being assigned (if by admin)
    project_id = request.data.get('project_id')
    
    logging.info(f"Received data: {user}", {project_id})
    print(f"Received data: {user.id, user.phone, user.role}", {project_id})

    # 1. Authorization Check: Is this an admin assigning another user?
    if assigned_user_id and user.role == 'admin':
        try:
            assigned_user = User.objects.get(id=assigned_user_id)
            logger.debug("Assigned user found: %s", assigned_user)
        except User.DoesNotExist:
            error_message = "Assigned user does not exist"
            logger.error(error_message)
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
        
        if assigned_user.role != 'stakeholder':
            error_message = "Assigned user must have the Stakeholder role"
            logger.error(error_message)
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

        stakeholder_user = assigned_user  # The user who will fund the project
    else:
        stakeholder_user = user
        if stakeholder_user.role != 'stakeholder':
            error_message = "You must be a Stakeholder to fund a project"
            logger.error(error_message)
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

    # 2. Stakeholder Registration Validation
    try:
        stakeholder = Stakeholder.objects.get(created_by=stakeholder_user)
        logger.debug("Stakeholder found: %s", stakeholder)
    except Stakeholder.DoesNotExist:
        error_message = "You must be registered as a Stakeholder to fund a project"
        logger.error(error_message)
        return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

    # 3. Planned Project Existence and Status Check
    try:
        planned_project = PlannedProject.objects.get(project__id=project_id, status='accepted')
        logger.debug("Planned project found: %s", planned_project)
    except PlannedProject.DoesNotExist:
        error_message = "Project not found or has not been accepted in Planned Projects"
        logger.error(error_message)
        return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
    
    if FundedProject.objects.filter(funded_project=planned_project, status='accepted'):
        error_message = "This project has been funded"
        logger.error(error_message)
        return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
    

    # 4. Uniqueness Check: Ensure the user has not already funded this project
    if FundedProject.objects.filter(created_by=stakeholder, funded_project=planned_project).exists():
        error_message = "You have already funded this project"
        logger.error(error_message)
        return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
    
    
    

    # If all checks pass, create the FundedProject record
    funded_project = FundedProject(created_by=stakeholder, funded_project=planned_project, status='pending')
    funded_project.save()
    logger.debug("Funded project created: %s", funded_project)

    # Update the Project's status to 'funded'
    project = planned_project.project
    project.status = 'in_progress'
    project.save()
    logger.debug("Project status updated to 'funded': %s", project)

    # Serialize and return the funded project details
    serializer = FundedProjectSerializer(funded_project)
    logger.info("Funded project serialized data: %s", serializer.data)
    return Response(serializer.data, status=status.HTTP_201_CREATED)






@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_funded_project_by_id(request, pk):
    try:
        funded_project = FundedProject.objects.get(pk=pk)
        serializer = FundedProjectSerializer(funded_project)
        return Response(serializer.data)
    except FundedProject.DoesNotExist:
        return Response({"error": "Funded project not found"}, status=status.HTTP_404_NOT_FOUND)





@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_funded_projects(request):
    funded_projects = FundedProject.objects.all()
    serializer = FundedProjectSerializer(funded_projects, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_funded_project(request, pk):
    try:
        funded_project = FundedProject.objects.get(pk=pk)
    except FundedProject.DoesNotExist:
        return Response({"error": "Funded project not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = FundedProjectSerializer(funded_project, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_funded_project(request, pk):
    try:
        funded_project = FundedProject.objects.get(pk=pk)
        funded_project.delete()
        return Response({"message": "Funded project deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except FundedProject.DoesNotExist:
        return Response({"error": "Funded project not found"}, status=status.HTTP_404_NOT_FOUND)







# Backend (views.py)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_funded_projects(request):
    try:
        # Get the stakeholder object for the logged-in user
        stakeholder = Stakeholder.objects.get(created_by=request.user)
        
        # Filter funded projects
        funded_projects = FundedProject.objects.filter(created_by=stakeholder)
        
        # Serialize the data
        serializer = FundedProjectSerializer(funded_projects, many=True)
        
        # Print the data to terminal
        print("\n=== Funded Projects Data ===")
        print(f"Total Projects Found: {len(serializer.data)}")
        for project in serializer.data:
            print("\nProject Details:")
            print(f"ID: {project['id']}")
            print(f"Status: {project['status']}")
            print(f"Created At: {project['created_at']}")
            print("\nStakeholder Details:")
            print(f"Email: {project['created_by']['email']}")
            print(f"Address: {project['created_by']['address']}")
            print(f"Monthly Income: {project['created_by']['monthly_income']}")
            print("\nFunded Project Details:")
            print(f"Duration: {project['funded_project']['duration']}")
            print(f"Cost: {project['funded_project']['cost']}")
            print(f"Location: {project['funded_project']['location']}")
            print("=" * 50)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Stakeholder.DoesNotExist:
        print("Error: Stakeholder not found for user")
        return Response(
            {"error": "You must be a registered stakeholder to view your funded projects."},
            status=status.HTTP_403_FORBIDDEN
        )