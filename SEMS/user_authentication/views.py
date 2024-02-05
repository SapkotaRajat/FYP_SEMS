# app/user_authentication/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm , LoginForm
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.forms import PasswordResetForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from .models import CustomUser

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
                    errors.append(errors[0])
                    print(field, errors)
            messages.error(request, form.errors['__all__'])

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
@login_required
def profile(request):
    return render(request, 'profile/profile.html', {})
@login_required
def change_password(request):
    # Implement your password reset logic here
    return render(request, 'change-password.html', {})



class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password-reset.html'
    success_url = reverse_lazy('password_reset_done')
    email_template_name = 'registration/password_reset_email.html'
    form_class = PasswordResetForm

    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        # Add your custom validation logic here
        email = form.cleaned_data['email']
        print(email)
        
        # Check if the email exists in the database
        if CustomUser.objects.filter(email=email).exists():
            # User is registered, proceed with the default behavior
            return super().form_valid(form)
        else:
            # User is not registered, add an error message
            messages.error(self.request, 'No accounts found with that email address.')
            # Render the form again with the error message
            return self.render_to_response(self.get_context_data(form=form))