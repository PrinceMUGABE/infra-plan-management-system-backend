# urls.py
from django.urls import path
from .views import (
    PlannedProjectCreateView,
    PlannedProjectListView,
    PlannedProjectRetrieveView,
    PlannedProjectUpdateView,
    PlannedProjectDeleteView,
    PlannedProjectByProjectView,
    PlannedProjectByPlannerView,
    accept_project,
    reject_project
)

urlpatterns = [
    path('projects/', PlannedProjectListView.as_view(), name='planned_project_list'),
    path('create/', PlannedProjectCreateView.as_view(), name='planned_project_create'),
    path('<int:pk>/', PlannedProjectRetrieveView.as_view(), name='planned_project_detail'),
    path('update/<int:pk>/', PlannedProjectUpdateView.as_view(), name='planned_project_update'),
    path('delete/<int:pk>/', PlannedProjectDeleteView.as_view(), name='planned_project_delete'),
    path('accept/<int:project_id>/', accept_project, name='accept_project'),
    path('reject/<int:project_id>/', reject_project, name='reject_project'),
    path('project/<int:project_id>/', PlannedProjectByProjectView.as_view(), name='planned_project_by_project'),
    path('planner/<int:planner_id>/', PlannedProjectByPlannerView.as_view(), name='planned_project_by_planner'),
]
