# event_management/views.py
from django.shortcuts import render, get_object_or_404
from .models import Category, Event , Organizer, EventVacancy
from django.utils import timezone
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from functools import wraps

def staff_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            from django.shortcuts import redirect
            # Redirect to login page or another appropriate page
            return redirect('custom_404')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def events_and_tickets(request):
    upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by('date')[:3]
    categories = Category.objects.all()
    return render(request, 'events-and-tickets.html', {'upcoming_events': upcoming_events , 'categories': categories})

def events_categories(request):
    # return categories in descending order by number of events
    categories = Category.objects.annotate(num_events=Count('event')).order_by('-num_events')
    return render(request, 'events-categories.html', {'categories': categories})

def event_details(request, event_id):
    # Retrieve the Event object corresponding to the event ID
    event = get_object_or_404(Event, pk=event_id)
    
    # Perform the comparison to determine if the event is over
    today = timezone.now().date()
    event.is_event_over = event.date < today
    
    # Pass the event object and today's date to the template context
    return render(request, 'event-details.html', {'event': event, 'today': today})


def events(request, category_name):
    category = Category.objects.get(name=category_name)
    # only pass the events that are not completed yet and are in the selected category
    events = Event.objects.filter(date__gte=timezone.now()).filter(category=category).order_by('date')
    return render(request, 'events.html', {'events': events , 'category': category})


def schedules(request):
    # return events in ascending order by date that are not completed yet
    events = Event.objects.filter(date__gte=timezone.now()).order_by('date')
    return render(request, 'schedules.html' , {'events': events})

def organizer_details(request, organizer_name):
    organizer = get_object_or_404(Organizer, organization=organizer_name)
    return render(request, 'organizer-details.html', {'organizer': organizer})

@login_required
@staff_required
def signup_events(request):
    current_time_plus_24_hours = timezone.now() + timedelta(hours=24)
    events = Event.objects.filter(date__gte=current_time_plus_24_hours).order_by('date')
    return render(request, 'signup-events.html', {'events': events})

@login_required
@staff_required
def signup_for_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    # return the vacancy form for the event EventVacancy
    vacancies = EventVacancy.objects.filter(event=event)
    return render(request, 'signup-for-event.html', {'vacancies': vacancies})

@login_required
def signup_for_vacancy(request, vacancy_id):
    vacancy = get_object_or_404(EventVacancy, pk=vacancy_id)

    if request.user.is_authenticated:
        if not vacancy.assigned_staff:  # Check if the vacancy is not already assigned
            vacancy.assigned_staff = request.user
            vacancy.save()

            # Log the event
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(vacancy).pk,
                object_id=vacancy.pk,
                object_repr=str(vacancy),
                action_flag=CHANGE,
                change_message=f"Staff member {request.user.username} signed up for position {vacancy.position.position} at event {vacancy.event.title}.",
            )
            messages.success(request, f"You have successfully signed up for the '{vacancy.position.position}' position at '{vacancy.event.title}'.")
        else:
            messages.error(request, "This position is already filled.")
    return redirect('signup-for-event', vacancy.event.id)

from django.http import HttpResponseForbidden

@login_required
@staff_required
def assigned_tasks(request):
    # Select the assigned tasks for the current user which are not completed yet
    vacancies = EventVacancy.objects.filter(
        assigned_staff=request.user,
        date__gte=timezone.now()
    ).order_by('date')
    
    return render(request, 'assigned-tasks.html', {'vacancies': vacancies})


@login_required
@staff_required
def work_history(request):
    # select the assigned tasks for the current user which are completed
    vacancies = EventVacancy.objects.filter(assigned_staff=request.user).filter(date__lt=timezone.now()).order_by('date')
    return render(request, 'work-history.html', {'vacancies': vacancies})
