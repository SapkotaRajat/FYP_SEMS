from django.shortcuts import render

# Create your views here.
def staff_management(request):
    return render(request, 'staff_management.html', {})