from django.shortcuts import render
from event_management.models import Category, Event
from django.utils import timezone
from django.http import HttpResponseRedirect
from .models import StaffApplication, Positions, PositionsCategory, Policy
from django.contrib.auth.decorators import login_required

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

@login_required
def staff_application(request):
    # pass the positions available to the form
    positions = Positions.objects.all()
    if request.method == 'POST':
        # create a new staff application
        staff_application = StaffApplication(
            position_desired=request.POST['position_desired'],
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            address=request.POST['address'],
            street_address=request.POST['street_address'],
            address_line_2=request.POST['address_line_2'],
            city=request.POST['city'],
            state_province_region=request.POST['state'],
            zip_postal_code=request.POST['zip_postal_code'],
            country=request.POST['country'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            referred_by=request.POST['referred_by'],
            convicted=True if request.POST.get('convicted') == 'yes' else False,
            convicted_explanation=request.POST['convicted_explanation'],
            school_name=request.POST['school_name'],
            highest_grade_completed=request.POST['highest_grade_completed'],
            graduate=True if request.POST.get('graduate') == 'yes' else False,
            # consent is checkbox 
            consent=True if request.POST.get('consent') == 'on' else False,
            resume=request.FILES['resume'],
            class_schedule=request.FILES['class_schedule']
        )
        staff_application.save()
        print(staff_application)
        return HttpResponseRedirect('/staff-application/success/')
    
    return render(request, 'staff-application.html', {'positions': positions})

def success(request):
    return render(request, 'success-page.html')