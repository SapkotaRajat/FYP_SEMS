from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import BuyTicketsForm
from .models import Ticket 
from event_management.models import Event

# Create your views here.
def ticket_purchase(request):
    tickets = Ticket.objects.all()
    return render(request, 'tickets.html' , {'tickets': tickets})

@login_required
def buy_tickets(request, event_name):
    event = Event.objects.get(title=event_name)    
    return render(request, 'buy-tickets.html', { 'event': event})

@login_required
def ticket_purchase_success(request):
    return render(request, 'ticket-purchase-success.html')
