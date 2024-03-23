# event_management/views.py
from django.shortcuts import render, get_object_or_404
from .models import Category, Event , Organizer
from django.utils import timezone
from django.db.models import Count
# Create your views here.

def events_and_tickets(request):
    upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by('date')[:3]
    categories = Category.objects.all()
    return render(request, 'events-and-tickets.html', {'upcoming_events': upcoming_events , 'categories': categories})

def events_categories(request):
    # return categories in descending order by number of events
    categories = Category.objects.annotate(num_events=Count('event')).order_by('-num_events')
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

def organizer_details(request, organizer_name):
    organizer = get_object_or_404(Organizer, organization=organizer_name)
    return render(request, 'organizer-details.html', {'organizer': organizer})