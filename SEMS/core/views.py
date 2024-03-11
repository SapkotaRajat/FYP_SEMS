from django.shortcuts import render
from event_management.models import Category, Event
from django.utils import timezone

def index(request):
    latest_event = Event.objects.filter(date__gte=timezone.now()).order_by('date').first()
    upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by('date')[:4]
    category = Category.objects.all()
    return render(request, 'index.html', {'latest_event': latest_event, 'category': category, 'upcoming_events': upcoming_events})

def custom_404(request, exception=None):
    return render(request, 'error.html', status=404)
def error(request):
    return render(request, 'error.html')
def plan_your_visit(request):
    return render(request, 'plan-your-visit.html')
def about(request):
    return render(request, 'about.html')
def policies(request):
    return render(request, 'policies.html')
def specifications(request):
    return render(request, 'specifications.html')
def employment(request):
    return render(request, 'employment.html')
def venue_booking(request):
    return render(request, 'venue-booking.html')
def contact_us(request):
    return render(request, 'contact-us.html')
def faq(request):
    return render(request, 'faq.html')
def terms_and_conditions(request):
    return render(request, 'terms-and-conditions.html')
def privacy_policy(request):
    return render(request, 'privacy-policy.html')
def refund_policy(request):
    return render(request, 'refund-policy.html')
