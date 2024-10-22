from django.urls import path
from .views import (
    ProjectCreateView, ProjectListView, ProjectDetailView, 
    ProjectUploadView, ProjectByStatusView, ProjectByFieldView, 
    ProjectDeleteView, ProjectUpdateView
)

urlpatterns = [
    path('create/', ProjectCreateView.as_view(), name='project-create'),
    path('projects/', ProjectListView.as_view(), name='project-list'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('upload/', ProjectUploadView.as_view(), name='project-upload'),
    path('status/', ProjectByStatusView.as_view(), name='project-by-status'),
    path('field/', ProjectByFieldView.as_view(), name='project-by-field'),
    path('delete/<int:pk>/', ProjectDeleteView.as_view(), name='project-delete'),
    path('update/<int:pk>/', ProjectUpdateView.as_view(), name='project-update'),  # New URL for project updating
]
