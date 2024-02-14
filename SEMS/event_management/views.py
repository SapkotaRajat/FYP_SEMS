# event_management/views.py
from django.shortcuts import render, get_object_or_404
from .models import Category, Event
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.

def events_and_tickets(request):
    upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by('date')[:3]
    return render(request, 'events-and-tickets.html', {'upcoming_events': upcoming_events})

def events_categories(request):
    categories = Category.objects.all()
    return render(request, 'events-categories.html', {'categories': categories})

def event_details(request, event_id):
    event = Event.objects.get(pk=event_id)
    return render(request, 'event-details.html', {'event': event})

def events(request, category_name):
    category = Category.objects.get(name=category_name)
    events = Event.objects.filter(category=category)
    return render(request, 'events.html', {'events': events , 'category': category})


def schedules(request):
    events = Event.objects.all()
    return render(request, 'schedules.html' , {'events': events})