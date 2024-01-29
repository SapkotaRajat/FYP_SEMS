from django.urls import path
from . import views

urlpatterns = [
    path('ticket_purchase/', views.ticket_purchase, name='ticket_purchase'),
    
]
