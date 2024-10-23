from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import PlannedProject
from .serializers import PlannedProjectSerializer, PlannedProjectDetailSerializer, DisplayPlannedProjectSerializer
import base64
import logging
from plannerApp.models import Planner



# Create logger
logger = logging.getLogger(__name__)

class PlannedProjectCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Decode the image if provided
        if 'image' in request.data:
            image_data = request.data['image']
            if image_data:
                try:
                    image_data = base64.b64decode(image_data)
                    request.data['image'] = image_data
                except base64.binascii.Error as e:
                    logger.error(f"Error decoding image: {str(e)}")
                    return Response({"error": "Invalid image format."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Ensure no duplicate plans for the same project by the same user
        project_id = request.data.get('project')
        user = request.user

        # Fetch the planner instance associated with the logged-in user
        try:
            planner = user.planner
        except Planner.DoesNotExist:
            logger.error(f"Planner instance does not exist for user {user.id}")
            return Response({"error": "Planner profile not found for this user."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if a planned project already exists for this project and planner
        if PlannedProject.objects.filter(project_id=project_id, planned_by=planner).exists():
            logger.warning(f"Planner {planner.id} attempted to create a duplicate plan for project {project_id}")
            return Response({"error": "You have already created a plan for this project."}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize and validate the planned project data
        serializer = PlannedProjectSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(planned_by=planner)  # Save with the associated planner
                logger.info(f"Planned project created successfully by planner {planner.id} for project {project_id}")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"Error saving planned project: {str(e)}")
                return Response({"error": "An error occurred while saving the planned project."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            logger.error(f"Validation error: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    

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


class PlannedProjectByPlannerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, planner_id):
        planned_projects = PlannedProject.objects.filter(planned_by__id=planner_id)
        serializer = DisplayPlannedProjectSerializer(planned_projects, many=True)
        return Response(serializer.data)





class PlannedProjectAcceptView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            planned_project = PlannedProject.objects.get(pk=pk)
            planned_project.status = 'accepted'
            planned_project.save()

            # Update the associated project's status to 'planned'
            if planned_project.planned_project:  # Assuming 'planned_project' is the related field for the Project
                project = planned_project.planned_project
                project.status = 'planned'
                project.save()

            return Response({"detail": "Project plan accepted and project status updated to planned."}, status=status.HTTP_200_OK)
        except PlannedProject.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class PlannedProjectRejectView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            planned_project = PlannedProject.objects.get(pk=pk)
            planned_project.status = 'rejected'
            planned_project.save()
            return Response({"detail": "Project plan rejected."}, status=status.HTTP_200_OK)
        except PlannedProject.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
