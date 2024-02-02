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
            messages.success(request, 'Registration successful')            
            # Redirect to the home page or another page after successful registration
            return redirect('login')
        else:
            # Display specific error messages for each field
            for field, errors in form.errors.items():
                print(field, errors)
                for error in errors:
                    # Set error messages for each form field
                    messages.error(request, f'{field}: {error}')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

def login_request(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                messages.error(request, 'Authentication failed')
        else:
            # Check for non-field errors and display the first one
            non_field_errors = form.errors.get('__all__')
            if non_field_errors:
                print(non_field_errors)
            else:
                for field, errors in form.errors.items():
                    print(field, errors)
            messages.error(request, 'Form validation failed')

    else:
        form = LoginForm()

    return render(request, 'login.html', {'login_form': form})

@login_required
def logout_request(request):
    logout(request)
    return redirect('login')

@login_required
def logout_confirmation(request):
    return render(request, 'logout.html')

def profile(request):
    return render(request, 'profile.html', {})

def change_password(request):
    # Implement your password reset logic here
    return render(request, 'change-password.html', {})