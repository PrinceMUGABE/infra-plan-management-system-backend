from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_application, name='create_application'),
    path('<int:application_id>/', views.get_application_by_id, name='get_application_by_id'),
    path('all/', views.get_all_applications, name='get_all_applications'),
    path('engineer/', views.get_all_applications_for_engineer, name='get_all_applications_for_engineer'),
    path('update/<int:application_id>/', views.update_application_status, name='update_application_status'),
    path('delete/<int:application_id>/', views.delete_application, name='delete_application'),
    path('accept/<int:application_id>/', views.accept_application, name='accept_application'),
    path('reject/<int:application_id>/', views.reject_application, name='reject_application'),
]
