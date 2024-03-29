from django.shortcuts import render
from event_management.models import Category, Event
from django.utils import timezone
from .models import PositionsCategory, Policy

def index(request):
    # return one random event on each load
    latest_event = Event.objects.order_by('?').first()
    upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by('date')[:4]
    category = Category.objects.all()
    return render(request, 'index.html', {'latest_event': latest_event, 'category': category, 'upcoming_events': upcoming_events})

def custom_404(request, exception=None):
    return render(request, 'error.html', status=404)
def error(request):
    return render(request, 'error.html')
def plan_your_visit(request):
    today = timezone.now().date()
    return render(request, 'plan-your-visit.html' , {'today': today})
def about(request):
    return render(request, 'about.html')
def policies(request):
    policies = Policy.objects.all()
    return render(request, 'policies.html' , {'policies': policies})
def specifications(request):
    return render(request, 'specifications.html')
def employment(request):
    categories = PositionsCategory.objects.all()
    return render(request, 'employment.html', {'categories': categories})
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

def thank_you(request):
    return render(request, 'thank-you.html')