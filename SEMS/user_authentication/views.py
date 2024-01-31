# app/user_authentication/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm , LoginForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Save the user to the database
            form.save()
            messages.success(request, 'Registration successful. Please log in.')
            # Redirect to the home page or another page after successful registration
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

def login_request(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                # Redirect to the home page or another page after successful login
                return redirect('index')
            else:
                # Add a message to indicate login failure if needed
                messages.error(request, 'Invalid email or password')
        else:
            # Handle form validation errors
            messages.error(request, 'Form validation failed')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'login_form': form})

@login_required
def logout_request(request):
    logout(request)
    # Redirect to the home page or another page after successful logout
    return redirect('index')

def forgot_password(request):
    # Implement your password reset logic here
    return render(request, 'forgot-password.html', {})
