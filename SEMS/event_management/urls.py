# event_management/urls.py
from django.urls import path    
from . import views

urlpatterns = [
    path('events-and-tickets/', views.events_and_tickets, name='events-and-tickets'),
    path('events-categories/', views.events_categories, name='events-categories'),
    path('events/<str:category_name>/', views.events, name='events'),
    path('event-details/<int:event_id>', views.event_details, name='event-details'),
    path('schedules/', views.schedules, name='schedules'),
    path('organizer-details/<str:organizer_name>', views.organizer_details, name='organizer-details'),
    path('events/', views.signup_events, name='events'),
    path('signup-for-event/<int:event_id>', views.signup_for_event, name='signup-for-event'),
    path('signup-for-vacancy/<int:vacancy_id>', views.signup_for_vacancy, name='signup-for-vacancy'),
    path('assigned-tasks/', views.assigned_tasks, name='assigned_tasks'),
    path('work_history/', views.work_history, name='work_history'),
    path('past-events/', views.past_events, name='past_events'),
]
    