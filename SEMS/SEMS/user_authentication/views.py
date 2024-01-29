from django.shortcuts import render

# Create your views here.
def register(request):
    return render(request, 'register.html', {})

def login_request(request):
    return render(request, 'login.html', {})

def logout_request(request):
    return render(request, 'logout.html', {})
