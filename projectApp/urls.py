from django.urls import path
from .views import (
    ProjectCreateView, ProjectListView, ProjectDetailView, 
    ProjectUploadView, ProjectByStatusView, ProjectByFieldView, 
    ProjectDeleteView, ProjectUpdateView,
    UserProjectListView
)

urlpatterns = [
    path('create/', ProjectCreateView.as_view(), name='project-create'),
    path('projects/', ProjectListView.as_view(), name='project-list'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('upload/', ProjectUploadView.as_view(), name='project-upload'),
    path('status/', ProjectByStatusView.as_view(), name='project-by-status'),
    path('field/', ProjectByFieldView.as_view(), name='project-by-field'),
    path('delete/<int:pk>/', ProjectDeleteView.as_view(), name='project-delete'),
    path('update/<int:pk>/', ProjectUpdateView.as_view(), name='project-update'),
    path('my-projects/', UserProjectListView.as_view(), name='user-projects'),
]
