from django.urls import path
from .views import (
    StakeholderCreateView,
    StakeholderDetailView,
    StakeholderByPhoneView,
    StakeholderByEmailView,
    StakeholderListView,
    StakeholderUpdateView,
    StakeholderDeleteView,
)

urlpatterns = [
    path('stakeholders/', StakeholderListView.as_view(), name='stakeholder-list'),
    path('create/', StakeholderCreateView.as_view(), name='stakeholder-create'),
    path('<int:pk>/', StakeholderDetailView.as_view(), name='stakeholder-detail'),
    path('update/<int:pk>/', StakeholderUpdateView.as_view(), name='stakeholder-update'),
    path('delete/<int:pk>/', StakeholderDeleteView.as_view(), name='stakeholder-delete'),
    path('phone/<str:phone>/', StakeholderByPhoneView.as_view(), name='stakeholder-by-phone'),
    path('email/<str:email>/', StakeholderByEmailView.as_view(), name='stakeholder-by-email'),
]
