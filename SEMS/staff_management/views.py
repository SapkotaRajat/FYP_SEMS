from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import StaffApplication
from core.models import Positions
from django.contrib.auth.decorators import login_required

def staff_management(request):
    return render(request, 'staff_management.html', {})

@login_required
def staff_application(request):
    user = request.user
    positions = Positions.objects.all()
    if request.method == 'POST':
        staff_application = StaffApplication(
            position_desired=request.POST['position_desired'],
            first_name=user.first_name,
            last_name=user.last_name,
            address=request.POST['address'],
            street_address=request.POST['street_address'],
            address_line_2=request.POST['address_line_2'],
            city=request.POST['city'],
            state_province_region=request.POST['state'],
            zip_postal_code=request.POST['zip_postal_code'],
            country=request.POST['country'],
            email=user.email,
            phone=request.POST['phone'],
            referred_by=request.POST['referred_by'],
            convicted=True if request.POST.get('convicted') == 'yes' else False,
            convicted_explanation=request.POST['convicted_explanation'],
            school_name=request.POST['school_name'],
            highest_grade_completed=request.POST['highest_grade_completed'],
            graduate=True if request.POST.get('graduate') == 'yes' else False,
            consent=True if request.POST.get('consent') == 'on' else False,
            resume=request.FILES['resume'],
            class_schedule=request.FILES['class_schedule']
        )
        staff_application.save()
        return HttpResponseRedirect('/thank-you/')
    
    return render(request, 'staff-application.html', {'positions': positions})
