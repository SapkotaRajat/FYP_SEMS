# event_management/views.py
from django.shortcuts import render, get_object_or_404
from .models import Category, Event
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.

def events_and_tickets(request):
    upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by('date')[:3]
    print(upcoming_events)
    return render(request, 'events-and-tickets.html', {'upcoming_events': upcoming_events})

def events_categories(request):
    categories = Category.objects.all()
    print(categories)
    return render(request, 'events-categories.html', {'categories': categories})

def event_details(request, event_id):
    event = Event.objects.get(pk=event_id)
    print(event)
    return render(request, 'event-details.html', {'event': event})

def events(request, category_name):
    category = Category.objects.get(name=category_name)
    events = Event.objects.filter(category=category)
    print(events)
    return render(request, 'events.html', {'events': events , 'category': category})
@login_required
def tickets(request,event_name):
    return render(request, 'tickets.html')