# event_management/views.py
from django.shortcuts import render, get_object_or_404
from .models import Category, Event , Organizer, EventVacancy
from django.utils import timezone
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.shortcuts import redirect
from django.contrib import messages

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
@login_required
def signup_events(request):
    current_time_plus_24_hours = timezone.now() + timedelta(hours=24)
    events = Event.objects.filter(date__gte=current_time_plus_24_hours).order_by('date')
    return render(request, 'signup-events.html', {'events': events})

def signup_for_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    # return the vacancy form for the event EventVacancy
    vacancies = EventVacancy.objects.filter(event=event)
    print(vacancies)
    
    return render(request, 'signup-for-event.html', {'vacancies': vacancies})
def signup_for_vacancy(request, vacancy_id):
    vacancy = get_object_or_404(EventVacancy, pk=vacancy_id)

    if request.user.is_authenticated:
        if not vacancy.assigned_staff:  # Check if the vacancy is not already assigned
            vacancy.assigned_staff = request.user
            vacancy.save()
            messages.success(request, f"You have successfully signed up for the '{vacancy.position.position}' position at '{vacancy.event.title}'.")
        else:
            messages.error(request, "This position is already filled.")
    else:
        messages.error(request, "You must be logged in to sign up for a vacancy.")
    print(vacancy.event.id)
    return redirect('signup-for-event', vacancy.event.id)