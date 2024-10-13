from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('users/', views.get_all_users, name='get_all_users'),
    path('user/<int:id>/', views.get_user_by_id, name='get_user_by_id'),
    path('username/<str:username>/', views.get_user_by_username, name='get_user_by_username'),
    path('email/<str:email>/', views.get_user_by_email, name='get_user_by_email'),
    path('update/<int:id>/', views.update_user_by_id, name='update_user_by_id'),
    path('delete/<int:id>/', views.delete_user_by_id, name='delete_user_by_id'),
    path('update-profile/<str:identifier>/', views.update_user_by_email_or_username, name='update_user_by_email_or_username'),
]
