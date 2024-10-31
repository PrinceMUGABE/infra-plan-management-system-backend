# funded_project_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_funded_project, name='create_funded_project'),
    path('<int:pk>/', views.get_funded_project_by_id, name='get_funded_project_by_id'),
    path('all/', views.get_all_funded_projects, name='get_all_funded_projects'),
    path('update/<int:pk>/', views.update_funded_project, name='update_funded_project'),
    path('delete/<int:pk>/', views.delete_funded_project, name='delete_funded_project'),
    path('my_projects/', views.get_user_funded_projects, name='user_funded_projects')
]
