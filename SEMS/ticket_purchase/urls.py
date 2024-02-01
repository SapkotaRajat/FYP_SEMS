from django.urls import path
from . import views

urlpatterns = [
    path('events-and-tickets/', views.ticket_purchase, name='events-and-tickets'),
]
