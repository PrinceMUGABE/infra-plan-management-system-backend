from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import PlannedProject
from .serializers import PlannedProjectSerializer, PlannedProjectDetailSerializer, DisplayPlannedProjectSerializer
import base64
import logging
from plannerApp.models import Planner
from userApp.models import User



# Create logger
logger = logging.getLogger(__name__)

class PlannedProjectCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Make a mutable copy of request data
        data = request.data.copy()

        # Extract data fields directly
        project_id = data.get('project')
        image_data = data.get('image')
        location = data.get('location')
        cost = data.get('cost')
        duration =data.get('duration')

        # Decode the image if provided
        if image_data:
            try:
                decoded_image_data = base64.b64decode(image_data)
            except base64.binascii.Error as e:
                logger.error(f"Error decoding image: {str(e)}")
                return Response({"error": "Invalid image format."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            decoded_image_data = None  # Set to None if no image provided

        # Fetch the planner instance associated with the logged-in user
        try:
            planner = request.user.planner
        except Planner.DoesNotExist:
            logger.error(f"Planner instance does not exist for user {request.user.id}")
            return Response({"error": "Planner profile not found for this user."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if a planned project already exists for this project and planner
        if PlannedProject.objects.filter(project_id=project_id, planned_by=planner).exists():
            logger.warning(f"Planner {planner.id} attempted to create a duplicate plan for project {project_id}")
            return Response({"error": "You have already created a plan for this project."}, status=status.HTTP_400_BAD_REQUEST)

        # Create and save the PlannedProject instance
        try:
            planned_project = PlannedProject.objects.create(
                project_id=project_id,
                planned_by=planner,
                image=decoded_image_data,  # Assign decoded image data here
                location=location,  # Other fields can be added directly
                cost=cost,
                duration=duration
            )
            logger.info(f"Planned project created successfully by planner {planner.id} for project {project_id}")
            return Response({
                "message": "Planned project created successfully.",
                "project_id": planned_project.project_id,
                "planned_by": planned_project.planned_by.id,
                "location": planned_project.location,
                "cost": planned_project.cost,
                "duration": planned_project.duration,
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error saving planned project: {str(e)}")
            return Response({"error": "An error occurred while saving the planned project."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  

class PlannedProjectListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        planned_projects = PlannedProject.objects.all()
        serializer = DisplayPlannedProjectSerializer(planned_projects, many=True)
        return Response(serializer.data)



class PlannedProjectRetrieveView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            planned_project = PlannedProject.objects.get(pk=pk)
            serializer = PlannedProjectDetailSerializer(planned_project)

            print(f"======= Trying to retrieve data for project plan of {id} ========= \n")
            logger.info(f" \n\n Serialized PlannedProject data: {serializer.data} \n\n")

    
            if planned_project.image:
                serializer.data['image'] = base64.b64encode(planned_project.image).decode('utf-8')

            return Response(serializer.data)

        except PlannedProject.DoesNotExist:
            logger.error("PlannedProject with id %s does not exist", pk)
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        
              

class PlannedProjectUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            planned_project = PlannedProject.objects.get(pk=pk)

            # Decode the image if provided
            if 'image' in request.data:
                image_data = request.data['image']
                if image_data:
                    image_data = base64.b64decode(image_data)
                    request.data['image'] = image_data

            serializer = PlannedProjectSerializer(planned_project, data=request.data, partial=True)  # Enable partial updates
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except PlannedProject.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
     
        

class PlannedProjectDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            planned_project = PlannedProject.objects.get(pk=pk)
            planned_project.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PlannedProject.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)






class PlannedProjectByProjectView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        planned_projects = PlannedProject.objects.filter(planned_project__id=project_id)
        serializer = PlannedProjectSerializer(planned_projects, many=True)
        return Response(serializer.data)




from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import PlannedProject
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
def accept_project(request, project_id):
    logger.info(f"Received request to accept project {project_id}")
    try:
        # Fetch the planned project
        project_plan = get_object_or_404(PlannedProject, id=project_id)
        
        # Set the planned project status to 'accepted'
        project_plan.status = 'accepted'
        project_plan.save()
        
        # Fetch the related project and update its status to 'planned'
        project = project_plan.project
        project.status = 'planned'
        project.save()

        logger.info(f'Project {project.id} status updated to "planned" after plan acceptance by planner {project_plan.planned_by.id}')
        return Response({'message': 'Project accepted and status updated successfully'})
    
    except Exception as e:
        logger.error(f"Error accepting project: {e}")
        return Response({'error': 'Error accepting project'}, status=400)



@api_view(['POST'])
def reject_project(request, project_id):
    logger.info(f"Received request to reject project {project_id}")
    try:
        project_plan = get_object_or_404(PlannedProject, id=project_id)
        project_plan.status = 'rejected'
        project_plan.save()

        logger.info(f'Project {project_plan.project.id} rejected by planner {project_plan.planned_by.id}')
        return Response({'message': 'Project rejected successfully'})

    except Exception as e:
        logger.error(f"Error rejecting project: {e}")
        return Response({'error': 'Error rejecting project'}, status=400)
















import logging
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Logger setup
logger = logging.getLogger(__name__)

class PlannedProjectByPlannerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, planner_id):
        # Log the user ID with both logger and print as a fallback
        logger.info(f"Received planner_id: {planner_id}")
        print(f"Received planner_id: {planner_id}")  # Fallback for direct terminal output
        
        user = request.user

        try:
            user = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            logger.error("Error: User not found")
            return Response({"error": "User not found"}, status=404)

        # Ensure a single planner instance
        planner = Planner.objects.filter(created_by=user).first()

        if not planner:
            logger.error("Error: Planner not found")
            return Response({"error": "Planner not found"}, status=404)

        # Fetch planned projects
        planned_projects = PlannedProject.objects.filter(planned_by=planner)
        logger.info(f"Planned projects fetched: {planned_projects.count()} items")
        print(f"Planned projects fetched: {planned_projects.count()} items")

        # Serialize the projects
        serializer = DisplayPlannedProjectSerializer(planned_projects, many=True)
        logger.info(f"Serialized data: {serializer.data}")

        return Response(serializer.data)



