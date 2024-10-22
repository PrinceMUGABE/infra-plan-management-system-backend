# urls.py
from django.urls import path
from .views import (
    CreateEngineerView,
    ListEngineerView,
    RetrieveEngineerView,
    RetrieveEngineerByEmailView,
    UpdateEngineerView,
    DeleteEngineerView
)

urlpatterns = [
    path('create/', CreateEngineerView.as_view(), name='create-engineer'),
    path('engineers/', ListEngineerView.as_view(), name='list-engineers'),
    path('<int:pk>/', RetrieveEngineerView.as_view(), name='retrieve-engineer'),
    path('email/<str:email>/', RetrieveEngineerByEmailView.as_view(), name='retrieve-engineer-email'),
    path('update/<int:pk>/', UpdateEngineerView.as_view(), name='update-engineer'),
    path('delete/<int:pk>/', DeleteEngineerView.as_view(), name='delete-engineer'),
]
