from django.urls import path
from . import views

urlpatterns = [
    path('system-dashboard/', views.admin_dashboard, name='admin_system_dashboard'),
]