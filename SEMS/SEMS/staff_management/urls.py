from django.urls import path
from . import views

urlpatterns = [
    path('staff_management/', views.staff_management, name='staff_management'),
    
]