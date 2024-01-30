from django.urls import path
from . import views

urlpatterns = [
    path('', views.staff_management, name='staff_management'),
    
]