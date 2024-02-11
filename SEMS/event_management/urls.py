# event_management/urls.py
from django.urls import path    
from . import views

urlpatterns = [
    path('events-and-tickets/', views.events_and_tickets, name='events-and-tickets'),
    path('events-categories/', views.events_categories, name='events-categories'),
    
]
    