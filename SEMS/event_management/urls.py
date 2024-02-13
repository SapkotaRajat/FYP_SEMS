# event_management/urls.py
from django.urls import path    
from . import views

urlpatterns = [
    path('events-and-tickets/', views.events_and_tickets, name='events-and-tickets'),
    path('events-categories/', views.events_categories, name='events-categories'),
    path('events/<str:category_name>/', views.events, name='events'),
    path('event-details/<int:event_id>', views.event_details, name='event-details'),
    path('tickets/<str:event_name>', views.tickets, name='tickets'),
]
    