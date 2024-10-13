# urls.py
from django.urls import path
from .views import (
    PlannerCreateView, 
    PlannerListView, 
    PlannerDetailView, 
    PlannerByEmailView, 
    PlannerUpdateView, 
    PlannerDeleteView
)

urlpatterns = [
    path('planners/', PlannerListView.as_view(), name='planner-list'),
    path('create/', PlannerCreateView.as_view(), name='planner-create'),
    path('planner/<int:pk>/', PlannerDetailView.as_view(), name='planner-detail'),
    path('email/<str:email>/', PlannerByEmailView.as_view(), name='planner-by-email'),
    path('update/<int:pk>/', PlannerUpdateView.as_view(), name='planner-edit'),
    path('delete/<int:pk>/', PlannerDeleteView.as_view(), name='planner-delete'),
]
